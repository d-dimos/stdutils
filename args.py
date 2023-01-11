import argparse
from argparse import Namespace
import yaml


def dict2namespace(input_config):
    namespace = argparse.Namespace()
    for key, value in input_config.items():
        if isinstance(value, dict):
            new_value = dict2namespace(value)
        else:
            new_value = value
        setattr(namespace, key, new_value)
    return namespace


def get_args(parser):
    args = parser.parse_args()
    with open(args.config, 'r') as stream:
        config = yaml.safe_load(stream)
    config = dict2namespace(config)
    return Namespace(**vars(args), **vars(config))
