import diceware
import argparse
def get_passphrase():

    options = diceware.handle_options(['--num', '10'])

    return diceware.get_passphrase(options)