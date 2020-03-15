import re
import datetime
from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError
from ..utils import *
from .. import models
from pyramid.security import forget
from pyramid.security import remember
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
)

STATUS_LABELS = {
    0: 'healthy',
    1: 'suspicious',
    2: 'infected',
    3: 'disinfected'
}

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
        'status': marker.status,
        'status_label': STATUS_LABELS[marker.status]
    }


def comment_to_dict(comment):
    return {
        'id': comment.id,
        'name': comment.name,
        'note': comment.email,
        'comment': comment.comment,
        'status': comment.status,
        'status_label': STATUS_LABELS[comment.status] if comment.status is not None else None,
        'commented_date': comment.created.strftime('%Y-%m-%d'),
    }


def locale_to_coords(locale):
    """Return a tuple of coordinates, coresponding to the default map location for the given locale."""
    return {
        'sl': (46.0, 14.5),
        'en': (52.0, -1.7),
    }[locale]


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home(request):
    lon, lat = locale_to_coords(request.locale_name)
    get_coordinates_from_address('Privoz 17c, Ljubljana')
    return {
        'isotoday': get_iso_date(),
        'gen_passphrase': get_passphrase(),
        'default_lat': lon,
        'default_lon': lat,
    }


@view_config(route_name='home', renderer='../templates/index.jinja2', request_method='POST')
def home_post(request):
    lon, lat = locale_to_coords(request.locale_name)

    passphrase = request.params['passphrase']
    passphrase = passphrase.strip()

    gen_passphrase = request.params['gen_passphrase']
    email = request.params['email']

    # Check if too short
    if len(passphrase) <= 16:
        print("pass too short")
        return {'isotoday': get_iso_date(),
                'gen_passphrase': get_passphrase()}

    if gen_passphrase == passphrase:
        print("pass is the same as generated pass - adding user")
        # Check if the generated pass was entered
        new_user = models.User(passphrase=passphrase, email=email)
        request.dbsession.add(new_user)
        request.dbsession.flush()

        headers = remember(request, new_user.id)
        return HTTPFound(location=request.route_url('add_marker'),
                         headers=headers)
    else:
        print("pass is different than generated - search user")
        # Try to existing find a user with passphrase
        user = request.dbsession.query(models.User).filter_by(
            passphrase=passphrase).first()

        if user is not None:
            print("found")
            # Check if user has email and if new email was provided
            EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
            if email and EMAIL_REGEX.match(email):
                # Use regex to check if email is valid
                user.email = email
                request.dbsession.flush()
            # Found previous user
            headers = remember(request, user.id)
            return HTTPFound(location=request.route_url('add_marker'),
                             headers=headers)
        else:
            print("not found")

    return {
        'isotoday': get_iso_date(),
        'gen_passphrase': get_passphrase(),
        'default_lat': lon,
        'default_lon': lat,
    }


@view_config(route_name='add_marker', renderer='../templates/add_marker.jinja2')
def add_marker(request):
    lon, lat = locale_to_coords(request.locale_name)

    if not request.authenticated_userid:
        raise HTTPFound(request.route_path('home'))

    return {
        'isotoday': get_iso_date(),
        'default_lat': lon,
        'default_lon': lat,
    }


@view_config(route_name='add_marker', xhr=True, renderer='json', request_method='POST')
def add_marker_post(request):

    if not request.authenticated_userid:
        raise HTTPFound(request.route_path('home'))

    latitude = request.params.get('lat')
    longitude = request.params.get('lon')
    name = request.params.get('name')
    note = request.params.get('note')
    status = request.params.get('status')
    status = int(status) if status != "" else None
    reported_date = parse_iso_date(request.params.get('reported_date'))

    new_marker = models.Marker(
        latitude=latitude,
        longitude=longitude,
        name=name,
        note=note,
        reported_date=reported_date,
        user_id=request.authenticated_userid,
        status=status
    )

    request.dbsession.add(new_marker)
    # Needed to get the ID
    request.dbsession.flush()

    return marker_to_dict(new_marker, request.authenticated_userid)


@view_config(route_name='remove_marker', xhr=True, renderer='json')
def remove_marker(request):
    marker_id = int(request.matchdict.get('marker_id'))
    marker = request.dbsession.query(models.Marker).filter_by(
        id=marker_id,
        user_id=request.authenticated_userid,
    ).first()

    if marker is not None:
        marker.deleted = True

    return {}


@view_config(route_name='list_markers', renderer='json')
def list_markers(request):
    min_date = request.params.get("min_date")
    max_date = request.params.get("max_date")
    only_owned = request.params.get("only_owned", False)

    db_markers = request.dbsession.query(
        models.Marker).filter_by(deleted=False)

    if min_date is not None:
        db_markers = db_markers.filter(models.Marker.reported_date >= min_date)
    if max_date is not None:
        db_markers = db_markers.filter(models.Marker.reported_date <= max_date)
    if only_owned:
        db_markers = db_markers.filter_by(user_id=request.authenticated_userid)

    markers = []
    for m in db_markers:
        mtd = marker_to_dict(m, request.authenticated_userid)

        db_comments = request.dbsession.query(models.Comment).filter_by(marker_id=mtd['id'])
        if min_date is not None:
            db_comments = db_comments.filter(models.Comment.created >= min_date)
        if max_date is not None:
            db_comments = db_comments.filter(models.Comment.created <= max_date)
        db_comments = db_comments.order_by(models.Comment.created)

        mtd['comments'] = [comment_to_dict(d) for d in db_comments]

        comments_status = [d['status'] for d in mtd['comments']
            if d['status'] is not None
                ]

        if len(comments_status) > 0:
            mtd['cur_status'] = comments_status[-1]

        mtd['cur_status_label'] = STATUS_LABELS[mtd.get('cur_status') or mtd['status']]

        markers.append(mtd)

    return markers

@view_config(route_name='search_address', xhr=True, request_method='POST', renderer='json')
def search_address(request):
    address = request.params.get('search')

    coordinates = get_coordinates_from_address(address)

    return {
        'lat': coordinates[0],
        'lon': coordinates[1],
    }


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    url = request.route_url('home')
    print("logged out")
    return HTTPFound(location=url, headers=headers)


@view_config(route_name='acme')
def acme(request):
    return Response('qsNO-zNzXSX4yMncMJARDqWEu5AThIYsy5eGseyxQKA.bxO0l_kg40uGCKYTyVY79r5ZUf-SN87ty2ERrJcxsfo')


@view_config(context=Exception)
def system_error_view(context, request):
    request.raven.captureException()

    return Response('There was an error. We are working on it.', 500)
