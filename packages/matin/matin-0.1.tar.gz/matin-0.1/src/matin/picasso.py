#%%
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
from matplotlib.pyplot import MultipleLocator
import os

plt.style.use('ggplot')
root = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(root, 'arial.ttf')

def get_font(path=FONT_PATH, font_size=12, font_color='black'):
    font = fm.FontProperties(fname=path)
    font.set_size(font_size)
    # font.set_color(font_color)
    return font


def ax_default_style(ax, font_size=12, font_color='black', show_grid=False, show_legend=False, ratio=1.0, **kwargs):
    '''
    render the axes to a defined style
    '''
    _font = get_font(font_size=font_size, font_color=font_color)
    ax.set_facecolor('white')
    bwith = 1
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)

    if show_legend:
        legend = ax.legend(prop=_font, labelcolor=font_color)
        frame = legend.get_frame()
        frame.set_alpha(0.8)
        frame.set_facecolor('white')

    if show_grid:
        ax.grid('on', color='#e6e6e6')
    else:
        ax.grid(False)

    for label in ax.get_xticklabels():
        label.set_fontproperties(_font)
        label.set_color(font_color)
    for label in ax.get_yticklabels():
        label.set_fontproperties(_font)
        label.set_color(font_color)
    ax.xaxis.get_label().set_fontproperties(_font)
    ax.yaxis.get_label().set_fontproperties(_font)
    ax.xaxis.get_label().set_color(font_color)
    ax.yaxis.get_label().set_color(font_color)

    # ax.set(aspect=1.0 / ax.get_data_ratio() * ratio)



def ax_lims(ax, lims=[0, 0, 0, 0], interval_xticks=None, interval_yticks=None):
    '''
    adjust x and y limits
    '''
    if lims[0] + lims[1] != 0:
        ax.set_xlim([lims[0], lims[1]])
    if lims[2] + lims[3] != 0:
        ax.set_ylim([lims[2], lims[3]])
    if interval_xticks is not None:
        ax.xaxis.set_major_locator(MultipleLocator(interval_xticks))
    if interval_yticks is not None:
        ax.yaxis.set_major_locator(MultipleLocator(interval_yticks))


if __name__ == '__main__':
    fig, axs = plt.subplots(1, 1, figsize=(5, 5), squeeze=False)
    ax = axs[0][0]
    ax.plot(np.arange(100), np.random.rand(100), marker='o', label='test')
    ax.set_xlabel('harmonic_mean_std')
    ax.set_ylabel('recall@1')
    ax_lims(ax, interval_xticks=20, interval_yticks=1)
    ax_default_style(ax, font_size=20)
