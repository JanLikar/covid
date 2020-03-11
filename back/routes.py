def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('add_marker', 'add-marker')
    config.add_route('remove_marker', 'remove-marker/{marker_id}')
    config.add_route('list_markers', 'list-markers')
