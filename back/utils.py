import diceware
import argparse
from . import models
def get_passphrase(request):

    options = diceware.handle_options(['--num', '3'])

    dupes = ['fake_pass']
    while len(dupes) > 0:
        passphrase = diceware.get_passphrase(options)
        # Check if already exists
        dupes = request.dbsession.query(models.User).filter_by(
            passphrase=passphrase).all()

    return passphrase