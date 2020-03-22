from pyramid.static import QueryStringConstantCacheBuster

import time


def includeme(config):
    config.add_static_view('static', 'static')
    config.add_cache_buster('static', QueryStringConstantCacheBuster(str(int(time.time()))))

    config.add_route('home', '/')
    config.add_route('logout', 'logout')

    config.add_route('add_marker', 'add-marker')
    config.add_route('remove_marker', 'remove-marker/{marker_id}')
    config.add_route('list_markers', 'list-markers')
    config.add_route('marker_popup', 'marker-popup/{marker_id}')
    config.add_route('add_comment', 'add-comment')
    config.add_route('search_address', 'search-address')

    config.add_route('embed_map', 'embed-map')

    config.add_route('acme', '.well-known/acme-challenge/qsNO-zNzXSX4yMncMJARDqWEu5AThIYsy5eGseyxQKA')
