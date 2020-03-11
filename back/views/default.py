import datetime
from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


def get_iso_date():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d')


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home(request):
    return {'isotoday': get_iso_date()}


@view_config(route_name='mark_location', renderer='../templates/mark_location.jinja2', request_method='GET')
def mark_location(request):
	return {'isotoday': get_iso_date()}


@view_config(route_name='mark_location', renderer='../templates/mark_location.jinja2', request_method='POST')
def mark_location_post(request):
	latitude = request.params.get('lat')
	longitude = request.params.get('lon')
	name = request.params.get('name')
	note = request.params.get('note')
	reported_date = datetime.date.today() #request.params.get('reported_date')

	request.dbsession.add(models.Marker(
		latitude=latitude,
		longitude=longitude,
		name=name,
		note=note,
		reported_date=reported_date,
	))

	return {'isotoday': get_iso_date()}


@view_config(route_name='list_locations', renderer='json')
def list_locations(request):
	markers = []

	for m in request.dbsession.query(models.Marker):
		markers.append({
			'lon': float(m.longitude),
			'lat': float(m.latitude),
			'name': m.name,
			'note': m.note,
			'reported_date': m.reported_date.strftime('%Y-%m-%d'),
		})


	return markers
