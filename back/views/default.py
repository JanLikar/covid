import datetime
from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


def get_iso_date():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d')


def marker_to_dict(marker):
	return {
		'id': marker.id,
		'lon': float(marker.longitude),
		'lat': float(marker.latitude),
		'name': marker.name,
		'note': marker.note,
		'reported_date': marker.reported_date.strftime('%Y-%m-%d'),
		'owned': False,
	}


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home(request):
    return {'isotoday': get_iso_date()}


@view_config(route_name='mark_location', renderer='../templates/mark_location.jinja2', request_method='GET')
def mark_location(request):
	return {'isotoday': get_iso_date()}


@view_config(route_name='mark_location', xhr=True, renderer='json', request_method='POST')
def mark_location_post(request):
	latitude = request.params.get('lat')
	longitude = request.params.get('lon')
	name = request.params.get('name')
	note = request.params.get('note')
	reported_date = datetime.date.today() #request.params.get('reported_date')

	new_marker = models.Marker(
		latitude=latitude,
		longitude=longitude,
		name=name,
		note=note,
		reported_date=reported_date,
		user_id=request.user_id,
	)

	request.dbsession.add(new_marker)
	# Needed to get the ID
	request.dbsession.flush()

	return marker_to_dict(new_marker)


@view_config(route_name='remove_marker', xhr=True, renderer='json')
def remove_marker(request):
	marker_id = int(request.matchdict.get('marker_id'))
	request.dbsession.query(models.Marker).filter_by(
		id=marker_id,
		user_id=request.user_id,
	).delete()

	return {}


@view_config(route_name='list_locations', renderer='json')
def list_locations(request):
	markers = []

	for m in request.dbsession.query(models.Marker):
		markers.append(marker_to_dict(m))


	return markers
