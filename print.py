from argparse import Namespace


def pretty(namespace, indent=0):
    output_text = ""
    for key, value in vars(namespace).items():
        output_text += ' ' * indent + str(key) + '\n'
        if isinstance(value, Namespace):
            output_text += pretty(value, indent + 3)
        else:
            output_text += ' ' * (indent + 3) + str(value) + '\n'
    return output_text
