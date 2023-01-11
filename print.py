from argparse import Namespace
import logging


def pretty(namespace, indent=0, logger=True):
    if logger:
        for key, value in vars(namespace).items():
            logging.info(' ' * indent + str(key))
            if isinstance(value, Namespace):
                logging.info(pretty(value, indent + 3))
            else:
                logging.info(' ' * (indent + 3) + str(value))
    else:
        output_text = ""
        for key, value in vars(namespace).items():
            output_text += ' ' * indent + str(key) + '\n'
            if isinstance(value, Namespace):
                output_text += pretty(value, indent + 3)
            else:
                output_text += ' ' * (indent + 3) + str(value) + '\n'
        return output_text
