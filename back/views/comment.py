import datetime
from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError
from ..utils import get_passphrase
from .. import models
from pyramid.security import forget
from pyramid.security import remember
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
)

from .default import parse_iso_date

@view_config(route_name='add_comment', request_method='POST')
def add_comment_post(request):
    name = request.params.get('name')
    email = request.params.get('email')
    comment = request.params.get('comment')
    marker_id = request.params.get('marker_id')
    user_id = request.params.get('user_id')
    status = request.params.get('status')
    created = parse_iso_date(request.params.get('created_date'))

    new_comment = models.Comment(
        name = name,
        email = email,
        comment = comment,
        marker_id = marker_id,
        user_id = request.authenticated_userid,
        created = created,
        status = status
    )

    request.dbsession.add(new_comment)
    # Needed to get the ID
    request.dbsession.flush()

    url = request.route_url('home')

    return HTTPFound(location=url)
