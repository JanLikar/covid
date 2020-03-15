from pyramid.config import Configurator
from pyramid_heroku import expandvars_dict
from pyramid.session import SignedCookieSessionFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""

    settings = expandvars_dict(settings)

    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('.i18n')
        config.include('pyramid_jinja2')
        config.include('pyramid_raven')
        config.include('.routes')
        config.include('.security')

        config.scan()

    # Defining sessions
    session_secret = settings['session.secret']
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    return config.make_wsgi_app()
