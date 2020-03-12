from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.security')

        config.add_translation_dirs('back:locale/')
        config.set_locale_negotiator(lambda r: 'en')

        config.scan()
    return config.make_wsgi_app()
