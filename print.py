from argparse import Namespace
import logging


def pretty(namespace, indent=0, logger=True):
    if logger:
        for key, value in vars(namespace).items():
            if value is None:
                continue
            logging.info(' ' * indent + str(key)+"{{{")
            if isinstance(value, Namespace):
                logging.info(pretty(value, indent + 2))
            else:
                logging.info(' ' * (indent + 2) + str(value))
    else:
        output_text = ""
        for key, value in vars(namespace).items():
            output_text += ' ' * indent + str(key) + '\n'
            if isinstance(value, Namespace):
                output_text += pretty(value, indent + 2)
            else:
                output_text += ' ' * (indent + 2) + str(value) + '\n'
        return output_text
