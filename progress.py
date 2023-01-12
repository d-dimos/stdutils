import numpy as np
import matplotlib.pyplot as plt


def plot_progress(args, mAP, rank1):
    x = mAP[args.data.targets[-1]]['euclidean'].iter_numbers

    for metric in [mAP, rank1]:
        plt.figure()
        for dataset in args.data.targets:
            y1 = 100 * np.array(metric[dataset]['euclidean'].val_storage)
            y2 = 100 * np.array(metric[dataset]['cosine'].val_storage)
            y1_avg = 100 * np.array(metric[dataset]['euclidean'].avg_storage)
            y2_avg = 100 * np.array(metric[dataset]['cosine'].avg_storage)

            plt.title('Mean Average Precision' if metric == mAP else 'CMC Curve - Rank 1')
            plt.plot(x, y1, label=f"{dataset} - eucl")
            plt.plot(x, y2, label=f"{dataset} - cos")
            plt.plot(x, y1_avg, label=f"{dataset} - eucl (avg)")
            plt.plot(x, y2_avg, label=f"{dataset} - cos (avg)")
            plt.ylim(0, 100)
            plt.yticks(np.arange(0, 100, step=10))
            plt.ylabel(f'{metric}')
            plt.xlim(0, args.num_iters)
            plt.xticks(np.arange(0, args.num_iters, step=args.eval_freq))
            plt.xlabel('#iter')
            plt.legend()

            plt.savefig(os.path.join(args.name, f'{metric}.png'))