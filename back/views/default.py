from datetime import datetime
from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


def get_iso_date():
    return datetime.utcnow().strftime('%Y-%m-%d')


@view_config(route_name='home', renderer='../templates/index.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(models.MyModel)
        one = query.filter(models.MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'isotoday': get_iso_date()}


@view_config(route_name='mark_location', renderer='../templates/mark_location.jinja2')
def mark_location(request):
	return {'isotoday': get_iso_date()}


@view_config(route_name='list_locations', renderer='json')
def list_locations(request):
	return [
		{'lon': 0.0, 'lat': 0.0, 'name': 'Some random location', 'note': 'I was there from 12:45 until 13:30.'},
		{'lon': 5.0, 'lat': 5.0, 'name': 'Some random location', 'note': 'I was there from 12:45 until 13:30.'},
	]


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
