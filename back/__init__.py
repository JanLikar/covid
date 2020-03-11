from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')

        config.add_translation_dirs('back:locale/')
        config.set_locale_negotiator(lambda r: 'en')

        setup_auth(config)

        config.scan()
    return config.make_wsgi_app()


def setup_auth(config):
	def get_user_id(request):
		return 1

	config.add_request_method(get_user_id, 'user_id', reify=True)
