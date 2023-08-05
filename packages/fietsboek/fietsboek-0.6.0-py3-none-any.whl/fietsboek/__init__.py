"""Fietsboek is a web application to track and share GPX tours.

This is the documentation for the Python package, useful for developers that
wish to work on fietsboek.

For more information, you can check out the following resources:

* The `Fietsboek repository`_.
* The documentation index: :doc:`../../../index`

.. _Fietsboek repository: https://gitlab.com/dunj3/fietsboek

Content
-------
"""
import importlib.metadata
from pathlib import Path
from typing import Callable, Optional

import redis
from pyramid.config import Configurator
from pyramid.csrf import CookieCSRFStoragePolicy
from pyramid.httpexceptions import HTTPServiceUnavailable
from pyramid.i18n import default_locale_negotiator
from pyramid.registry import Registry
from pyramid.request import Request
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory

from . import config as mod_config
from . import jinja2 as mod_jinja2
from . import transformers
from .data import DataManager
from .pages import Pages
from .security import SecurityPolicy

__VERSION__ = importlib.metadata.version("fietsboek")


def locale_negotiator(request: Request) -> Optional[str]:
    """Negotiates the right locale to use.

    This tries the following:

    1. It runs the default negotiator. This allows the locale to be overriden
       by using the ``_LOCALE_`` query parameter.
    2. It uses the `Accept-Language`_ header.

    .. _Accept-Language: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language

    :param request: The request for which to get the language.
    :return: The determined locale, or ``None`` if the default should be used.
    """
    locale = default_locale_negotiator(request)
    if locale:
        return locale

    installed_locales = request.config.available_locales
    sentinel = object()
    negotiated = request.accept_language.lookup(installed_locales, default=sentinel)
    if negotiated is sentinel:
        return None
    return negotiated


def maintenance_mode(
    handler: Callable[[Request], Response], _registry: Registry
) -> Callable[[Request], Response]:
    """A Pyramid Tween that handles the maintenance mode.

    Note that we do this as a tween to ensure we check for the maintenance mode
    as early as possible. This avoids hitting the DB, which might be in an
    inconsistent state.

    :param handler: The next handler in the tween/view chain.
    :param registry: The application registry.
    """

    def tween(request: Request) -> Response:
        maintenance = request.data_manager.maintenance_mode()
        if maintenance is None:
            return handler(request)

        return HTTPServiceUnavailable(
            f"This fietsboek is currently in maintenance mode: {maintenance}",
        )

    return tween


def main(_global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    # Avoid a circular import by not importing at the top level
    # pylint: disable=import-outside-toplevel,cyclic-import
    from .views.tileproxy import TileRequester

    parsed_config = mod_config.parse(settings)
    settings["jinja2.newstyle"] = True

    def data_manager(request):
        return DataManager(Path(request.config.data_dir))

    def redis_(request):
        return redis.from_url(request.config.redis_url)

    def config_(_request):
        return parsed_config

    # Load the pages
    page_manager = Pages()
    for path in parsed_config.pages:
        path = Path(path)
        if path.is_dir():
            page_manager.load_directory(path)
        elif path.is_file():
            page_manager.load_file(path)

    def pages(_request):
        return page_manager

    my_session_factory = SignedCookieSessionFactory(parsed_config.derive_secret("sessions"))
    cookie_secret = parsed_config.derive_secret("auth-cookie")
    with Configurator(settings=settings) as config:
        config.include("pyramid_jinja2")
        config.include(".routes")
        config.include(".models")
        config.add_tween(".maintenance_mode")
        config.scan()
        config.add_translation_dirs("fietsboek:locale/")
        for pack in parsed_config.language_packs:
            config.add_translation_dirs(f"{pack}:locale/")
        config.set_session_factory(my_session_factory)
        config.set_security_policy(SecurityPolicy(cookie_secret))
        config.set_csrf_storage_policy(CookieCSRFStoragePolicy())
        config.set_default_csrf_options(require_csrf=True)
        config.set_locale_negotiator(locale_negotiator)
        config.add_request_method(data_manager, reify=True)
        config.add_request_method(pages, reify=True)
        config.add_request_method(redis_, name="redis", reify=True)
        config.add_request_method(config_, name="config", reify=True)

    config.registry.registerUtility(TileRequester())

    jinja2_env = config.get_jinja2_environment()
    jinja2_env.filters["format_decimal"] = mod_jinja2.filter_format_decimal
    jinja2_env.filters["format_datetime"] = mod_jinja2.filter_format_datetime
    jinja2_env.filters["local_datetime"] = mod_jinja2.filter_local_datetime
    jinja2_env.globals["embed_tile_layers"] = mod_jinja2.global_embed_tile_layers
    jinja2_env.globals["list_transformers"] = transformers.list_transformers

    return config.make_wsgi_app()
