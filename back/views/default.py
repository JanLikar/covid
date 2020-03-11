import datetime
from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError
from ..utils import get_passphrase
from .. import models


def get_iso_date():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d')


def parse_iso_date(date):
	return datetime.datetime.strptime(date, '%Y-%m-%d').date()


def marker_to_dict(marker, user_id):
	return {
		'id': marker.id,
		'lon': float(marker.longitude),
		'lat': float(marker.latitude),
		'name': marker.name,
		'note': marker.note,
		'reported_date': marker.reported_date.strftime('%Y-%m-%d'),
		'owned': marker.user_id == user_id,
	}


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home(request):

    passphrase = get_passphrase()

    return {'isotoday': get_iso_date(),
            'passphrase': passphrase}

@view_config(route_name='home', renderer='../templates/index.jinja2',request_method='POST')
def my_view_handler(request):

    passphrase = request.params['passphrase']

    import pdb; pdb.set_trace()



    return {'isotoday': get_iso_date(),
            'passphrase': passphrase}

@view_config(route_name='mark_location', renderer='../templates/mark_location.jinja2')
def mark_location(request):
	return {'isotoday': get_iso_date()}


@view_config(route_name='add_marker', xhr=True, renderer='json', request_method='POST')
def add_marker_post(request):
	latitude = request.params.get('lat')
	longitude = request.params.get('lon')
	name = request.params.get('name')
	note = request.params.get('note')
	reported_date = parse_iso_date(request.params.get('reported_date'))

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

	return marker_to_dict(new_marker, request.user_id)


@view_config(route_name='remove_marker', xhr=True, renderer='json')
def remove_marker(request):
	marker_id = int(request.matchdict.get('marker_id'))
	request.dbsession.query(models.Marker).filter_by(
		id=marker_id,
		user_id=request.user_id,
	).delete()

	return {}


@view_config(route_name='list_markers', renderer='json')
def list_markers(request):
	markers = []

	for m in request.dbsession.query(models.Marker):
		markers.append(marker_to_dict(m, request.user_id))


	return markers
