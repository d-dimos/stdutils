import os


def create_dirs(args):
    if not os.path.exists(args.name):
        os.makedirs(args.name)
        return True
    return False
