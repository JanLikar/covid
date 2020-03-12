from pyramid.i18n import default_locale_negotiator
from pyramid.settings import aslist


def locale_negotiator(request):
    available_locales = aslist(request.registry.settings['available_locales'])
    default_locale = request.registry.settings['pyramid.default_locale_name']
    locale = default_locale_negotiator(request)

    if locale in available_locales:
        return locale

    return request.accept_language.best_match(available_locales, default_locale)


def includeme(config):
    config.add_translation_dirs('back:locale/')
    config.set_locale_negotiator(locale_negotiator)
