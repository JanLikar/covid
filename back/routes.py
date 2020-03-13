def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('logout', 'logout')

    config.add_route('add_marker', 'add-marker')
    config.add_route('remove_marker', 'remove-marker/{marker_id}')
    config.add_route('list_markers', 'list-markers')

    config.add_route('acme', '.well-known/acme-challenge/qsNO-zNzXSX4yMncMJARDqWEu5AThIYsy5eGseyxQKA')
