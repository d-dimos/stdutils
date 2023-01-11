import logging
import os


def configure_logger(args, level=20):
    handler1 = logging.StreamHandler()
    handler2 = logging.FileHandler(os.path.join(args.exp_dir, 'log.txt'))
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler1.setFormatter(formatter)
    handler2.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    logger.setLevel(level)
    return
