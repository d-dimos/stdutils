from argparse import Namespace
import logging


def pretty(namespace, indent=0):
    for key, value in vars(namespace).items():
        output_text = ' ' * indent + str(key) + ': '
        # logging.info(' ' * indent + str(key))
        if isinstance(value, Namespace):
            logging.info(output_text)
            pretty(value, indent + 2)
        else:
            logging.info(' ' * (indent + 2) + output_text + str(value))
