import os
import logging
import torch


def save_checkpoint(state, exp_name, epoch=-1, iteration=-1):
    if epoch == -1:
        filename = f'checkpoint_final.pth.tar'
    else:
        filename = f'checkpoint_e{epoch}_i{iteration}.pth.tar'
    directory = os.path.join(exp_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, filename)
    torch.save(state, filename)
    logging.info(f'Saved {filename}')
