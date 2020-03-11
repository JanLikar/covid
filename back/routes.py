def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('mark_location', 'mark_location')
    config.add_route('remove_marker', 'remove-marker/{marker_id}')
    config.add_route('list_locations', 'list_locations')
