import matplotlib.pyplot as plt
from PIL import Image
from os.path import join


def save_plots(filename, mse_list_dict):
    crowns = mse_list_dict.keys()

    quotient, remainder = len(crowns)//4, len(crowns) % 3

    rows = quotient
    columns = 4

    if remainder != 0:
        rows = quotient + 1

    fig = plt.figure(figsize=(columns * 10, rows * 7))

    i = 0
    for crown in crowns:
        ax = fig.add_subplot(rows, columns, i + 1)
        plt.title(crown, fontsize=16)
        plt.ylabel("MSE", fontsize=12)
        plt.xlabel("Files", fontsize=12)
        ax.plot(list(mse_list_dict[crown].keys()), list(mse_list_dict[crown].values()), linewidth=2)
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        ax.yaxis.grid(linestyle='dashed', linewidth=0.5)
        i += 1

    fig.savefig(join('saved_files', filename, 'mse_plots.png'), format='png', dpi=150)
    print('Plots saved: ' + join('saved_files', filename, 'mse_plots.png'))

    img = Image.open(join('saved_files', filename, 'mse_plots.png'))
    img.show()
