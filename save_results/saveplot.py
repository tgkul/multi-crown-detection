import matplotlib.pyplot as plt
from os.path import join


def save_plots(mse_list_dict):
    crowns = mse_list_dict.keys()
    for crown in crowns:
        fig = plt.figure(figsize=(50, 25))
        ax = fig.add_subplot(1, 1, 1)
        plt.title(crown, fontsize=40)
        plt.ylabel("Error", fontsize=40)
        plt.xlabel("Files", fontsize=40)
        ax.plot(list(range(len(mse_list_dict[crown]))), mse_list_dict[crown], linewidth=0.5)
        plt.savefig(join('saved_files', crown + '.pdf'), format='pdf', dpi=1200)
        print('Plots saved: ' + join('saved_files', crown + '.pdf'))
