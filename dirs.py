import os


def create_dirs(args):
    source_dataset = args.sources[0] if isinstance(args.sources, list) else args.sources
    args.exp_dir = os.path.join(args.name, source_dataset)
    args.name = args.config[:-4]
    if not os.path.exists(args.exp_dir):
        os.makedirs(args.exp_dir)
        return True
    return False
