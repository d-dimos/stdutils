class AverageMeter(object):
    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
        self.val_storage = []
        self.avg_storage = []
        self.iter_numbers = []

    def update(self, val, n=1, iter_num=0):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
        self.val_storage.append(self.val)
        self.avg_storage.append(self.avg)
        self.iter_numbers.append(iter_num)

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
        self.val_storage = []
        self.avg_storage = []
        self.iter_numbers = []