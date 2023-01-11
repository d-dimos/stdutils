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


def init_meter(targets):
    return {target: {metric: AverageMeter() for metric in dist_metrics} for target in targets}


def evaluate(args, name, model, g_loader, q_loader, mAP, rank1, iter_num=0):
    cmc_euclidean, mAP_euclidean = calculate_map_cmc(model, g_loader, q_loader, 'euclidean', args.test.normalize_feat)
    cmc_cosine, mAP_cosine = calculate_map_cmc(model, g_loader, q_loader, 'cosine', args.test.normalize_feat)
    logging.info(f'Evaluation on: {name}')
    logging.info(f'mAP:\t (euclidean) {mAP_euclidean:.1%}\t (cosine) {mAP_cosine:.1%}')
    ranks = [1, 5, 10]
    for r in ranks:
        logging.info(
            f'Rank-{r:<3}:\t (euclidean) {cmc_euclidean[r - 1]:.1%}\t (cosine) {cmc_cosine[r - 1]:.1%}'
        )
    mAP[name]['euclidean'].update(mAP_euclidean, args.test.batch_size, iter_num=iter_num)
    mAP[name]['cosine'].update(mAP_cosine, args.test.batch_size, iter_num=iter_num)
    rank1[name]['euclidean'].update(cmc_euclidean[0], args.test.batch_size, iter_num=iter_num)
    rank1[name]['cosine'].update(cmc_cosine[0], args.test.batch_size, iter_num=iter_num)


def calculate_map_cmc(model, gallery_loader, query_loader, dist_metric, normalize_feat):

    def extract(loader):
        f_, pids_, camids_ = [], [], []
        for batch_idx, data in enumerate(loader):
            imgs, pids, camids = data['img'], data['pid'], data['camid']
            imgs = imgs.cuda()
            params = list(model.parameters())
            features = model.functional(params, True, imgs, mix=True,
                                        return_featuremaps=True, noise_layer=True, eval=True)[2]

            features = features.cpu()
            f_.append(features)
            pids_.extend(pids.tolist())
            camids_.extend(camids.tolist())
        f_ = torch.cat(f_, 0)
        pids_ = np.asarray(pids_)
        camids_ = np.asarray(camids_)
        return f_, pids_, camids_

    query_feats, query_pids, query_camids = extract(query_loader)
    gallery_feats, gallery_pids, gallery_camids = extract(gallery_loader)

    if normalize_feat:
        query_feats = F.normalize(query_feats, p=2, dim=1)
        gallery_feats = F.normalize(gallery_feats, p=2, dim=1)

    distmat = torchreid.metrics.compute_distance_matrix(query_feats, gallery_feats, dist_metric)
    distmat = distmat.numpy()

    cmc, map = torchreid.metrics.evaluate_rank(distmat, query_pids, gallery_pids, query_camids, gallery_camids,
                                               use_metric_cuhk03=False)

    return cmc, map


def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res
