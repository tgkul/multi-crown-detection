import matplotlib.pyplot as plt
from os.path import join


def save_plots(mse_list_dict):
    crowns = mse_list_dict.keys()

    quotient, remainder = len(crowns)//3, len(crowns) % 3

    rows = quotient
    columns = 3

    if remainder != 0:
        rows = quotient + 1

    plt.figure(figsize=(columns * 10, rows * 7))

    i = 0

    for crown in crowns:
        ax = plt.subplot(rows, columns, i + 1)
        plt.title(crown, fontsize=16)
        plt.ylabel("MSE", fontsize=12)
        plt.xlabel("Files", fontsize=12)
        ax.plot(list(mse_list_dict[crown].keys()), list(mse_list_dict[crown].values()), linewidth=2)
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        ax.yaxis.grid(linestyle='dashed', linewidth=0.002)
        i += 1

    plt.savefig(join('saved_files', 'mse_plots.pdf'), format='pdf', dpi=1200)
    print('Plots saved: ' + join('saved_files', crown + '.pdf'))
