import diceware
import argparse
from . import models


def get_passphrase():
    options = diceware.handle_options(['--num', '4'])

    return diceware.get_passphrase(options)
