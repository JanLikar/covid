from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('.i18n')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.security')

        config.scan()
    return config.make_wsgi_app()
