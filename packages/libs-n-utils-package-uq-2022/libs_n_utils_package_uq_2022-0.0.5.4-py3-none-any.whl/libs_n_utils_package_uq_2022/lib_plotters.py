import dill
import pandas as pd
import seaborn as sns
import numpy as np
import os
import config_template
import matplotlib.transforms
from matplotlib import pyplot as plt
from plotly import express as px
from my_easy_logger import logger_cleaner
from lib_small_utils import random_hex_color


param_dic = config_template.plot_parameters.CDFplot_params_dic
dataset_colors = config_template.plot_parameters.dataset_colors

filename = os.path.split(__file__)[1]
info_log_color = 'purple,bg_yellow'




# ######################################################################################################################
@logger_cleaner
def draw_grouped_boxplot(_lists, _labels=None, _title_text=None, _save_address=None, _xlog_scale=None, _xlabel=None,
                         _ylabel=None, _different_group=None, _ylog_scale=None, _xticks=None, _yticks=None,
                         _first_group_color=None, _second_group_color=None, _xticks_rotation=None,
                         _xticklabel_size=None, _xlims=None, _ylims=None, _yticks_rotation=None, _yticklabel_size=None,
                         _fig_size=None, _title_fontsize=10, _xlabel_fontsize=10, _ylabel_fontsize=10, **kwargs):
    logger_ = kwargs['logger']

    logger_.info('plotting the boxplot ...')
    if _labels is None:
        _labels = list(range(len(_lists)))
    if _different_group is None:
        _different_group = []
    if _first_group_color is None:
        _first_group_color = 'lightgreen'
    if _second_group_color is None:
        _second_group_color = 'gold'

    flier_props = dict(marker='x', markersize=3)
    median_props = dict(linewidth=1, color='red')
    if _fig_size is None:
        plt.figure(figsize=(15, 10))
    else:
        plt.figure(figsize=(_fig_size[0], _fig_size[1]))
    boxes = plt.boxplot(_lists, labels=_labels, vert=False, patch_artist=True,
                        flierprops=flier_props, medianprops=median_props)

    logger_.info('Customizing the patches in boxplot ...')
    for patch_no in range(len(boxes['boxes'])):
        patch = boxes['boxes'][patch_no]
        if _labels[patch_no] not in _different_group:
            patch.set_facecolor(_first_group_color)
        else:
            patch.set_facecolor(_second_group_color)

    plt.grid(color='#BBBBBB', linestyle=':', linewidth=0.8)
    plot_helper(plt, _title_text=_title_text, _xlabel=_xlabel, _ylabel=_ylabel, _xticks=_xticks, _yticks=_yticks,
                _xlims=_xlims, _ylims=_ylims, _xlog_scale=_xlog_scale, _xticks_rotation=_xticks_rotation,
                _ylog_scale=_ylog_scale, _xticklabel_size=_xticklabel_size, _yticklabel_size=_yticklabel_size,
                _yticks_rotation=_yticks_rotation, _title_fontsize=_title_fontsize, _xlabel_fontsize=_xlabel_fontsize,
                _ylabel_fontsize=_ylabel_fontsize)

    if _save_address is not None:
        plt.savefig(_save_address, bbox_inches='tight')
        plt.close()
        logger_.info(f'Figure saved to {_save_address}.')
    else:
        plt.ion()
        plt.show()


# ######################################################################################################################
@logger_cleaner
def draw_histogram(_statistic_series, _hist_bins=None, _save_address=None, _title_text_=None, _yticks_rotation=None,
                   _xlabel=None, _ylabel=None, _xticks=None, _yticks=None, _hatch_pattern='None', _yticklabel_size=None,
                   _edge_color='None', _face_color='None', _xlims=None, _ylims=None, _xticklabel_size=None,
                   _ylog_scale=False, _xticks_rotation=0, _bin_width=None, _xlog_scale=False, _fig_size=None,
                   _title_fontsize=10, _xlabel_fontsize=10, _ylabel_fontsize=10, **kwargs):
    logger_ = kwargs['logger']
    if _fig_size is None:
        plt.figure(figsize=(15, 10))
    else:
        plt.figure(figsize=(_fig_size[0], _fig_size[1]))

    logger_.info('Computing histograms')
    if _hist_bins is None:
        hists = plt.hist(_statistic_series, bins='auto')
    else:
        if _bin_width is None:
            _bin_width = 1 / len(_hist_bins)
        hists = plt.hist(_statistic_series, bins=_hist_bins, rwidth=_bin_width)

    logger_.info('Histograms are now generated.')
    plt.grid(color='#999999', linestyle=':', linewidth=0.7, axis='y')
    if (_face_color != 'None') or (_edge_color != 'None') or (_hatch_pattern != 'None'):
        logger_.info(f'Customizing the appearance for {len(hists[2])} patches...')
        for patch_no in range(len(hists[2])):
            patch = hists[2][patch_no]
            if _face_color != 'None':
                patch.set_facecolor(_face_color)
            if _hatch_pattern != 'None':
                patch.set_hatch(_hatch_pattern)
            if _edge_color != 'None':
                patch.set_edgecolor(_edge_color)
    plot_helper(plt, _title_text=_title_text_, _xlabel=_xlabel, _ylabel=_ylabel, _xticks=_xticks, _yticks=_yticks,
                _xlims=_xlims, _ylims=_ylims, _xlog_scale=_xlog_scale, _xticks_rotation=_xticks_rotation,
                _ylog_scale=_ylog_scale, _xticklabel_size=_xticklabel_size, _yticklabel_size=_yticklabel_size,
                _yticks_rotation=_yticks_rotation, _title_fontsize=_title_fontsize, _xlabel_fontsize=_xlabel_fontsize,
                _ylabel_fontsize=_ylabel_fontsize, **kwargs)

    if _save_address is not None:
        plt.savefig(_save_address, bbox_inches='tight')
        plt.close()
        logger_.info(f'histogram saved to {_save_address}.')
    else:
        plt.ion()
        plt.show()


# ######################################################################################################################
@logger_cleaner
def draw_pie_chart(_data_object, _values=None, _labels=None, _title_text=None, _save_address=None, **kwargs):
    logger_ = kwargs['logger']
    if _values is None:
        _values = _data_object.value_counts()
    if _labels is None:
        _labels = _data_object.value_counts().index

    logger_.info('computing the pie-charts started ...')
    fig = px.pie(_data_object, values=_values, names=_labels, title=_title_text)
    fig.update_traces(hoverinfo='label+percent',
                      hole=.4, textinfo='label+percent', textposition='inside',
                      marker=dict(line=dict(color='#000000', width=1)))
    fig.write_html(_save_address)
    logger_.info(f'Pie chart saved to: {_save_address}')


# ######################################################################################################################
@logger_cleaner
def draw_bar_chart(_x_values, _y_values, *args, _save_address=None, _title_text=None, _xlabel=None, _ylabel=None,
                   _xticks=None, _yticks=None, _hatch_pattern='None', _edge_color='None', _face_color='None',
                   _xlims=None, _ylims=None, _figsize=None, _xlog_scale=False, _xticks_rotation=0, _bar_width=None,
                   _ylog_scale=False, _xticklabel_size=None, _xticks_rotation_dic=None, _yticklabel_size=None,
                   _yticks_rotation=None, _yticks_rotation_dic=None, _title_fontsize=10, _xlabel_fontsize=10,
                   _ylabel_fontsize=10, **kwargs):
    logger_ = kwargs['logger']
    if 'plt_handle' not in kwargs:
        plt_ = plt
        if _figsize is None:
            plt_.figure(figsize=(15, 10))
        else:
            plt_.figure(figsize=(_figsize[0], _figsize[1]))
    else:
        plt_ = kwargs['plt_handle']
        kwargs.pop('plt_handle')

    logger_.info('Plotting bar charts ...')
    if _bar_width is None:
        plb = plt_.bar(_x_values, _y_values)
    else:
        plb = plt_.bar(_x_values, _y_values, width=_bar_width)

    logger_.info('Bar charts are now generated.')
    plt_.grid(color='#999999', linestyle=':', linewidth=0.7, axis='y')
    if (_face_color != 'None') or (_edge_color != 'None') or (_hatch_pattern != 'None'):
        logger_.info(f'Customizing the appearance for {len(plb)} patches...')
        for patch_no in range(len(plb)):
            patch = plb[patch_no]
            if _face_color != 'None':
                patch.set_facecolor(_face_color)
            if _hatch_pattern != 'None':
                patch.set_hatch(_hatch_pattern)
            if _edge_color != 'None':
                patch.set_edgecolor(_edge_color)

            if '_xticks_rotation' in kwargs:
                _xticks_rotation = kwargs['_xticks_rotation']

    plot_helper(plt_, _title_text=_title_text, _xlabel=_xlabel, _ylabel=_ylabel, _xticks=_xticks, _yticks=_yticks,
                _xlims=_xlims, _ylims=_ylims, _xlog_scale=_xlog_scale, _xticks_rotation=_xticks_rotation,
                _ylog_scale=_ylog_scale, _xticklabel_size=_xticklabel_size, _yticklabel_size=_yticklabel_size,
                _yticks_rotation=_yticks_rotation, _title_fontsize=_title_fontsize, _xlabel_fontsize=_xlabel_fontsize,
                _ylabel_fontsize=_ylabel_fontsize, _xticks_rotation_dic=_xticks_rotation_dic,
                _yticks_rotation_dic=_yticks_rotation_dic, **kwargs)

    if _save_address is not None:
        plt_.savefig(_save_address, bbox_inches='tight')
        plt_.close()
        logger_.info(f'Bar chart saved to {_save_address}.')
    elif 'not_show' not in args:
        plt_.ion()
        plt_.show()


# ######################################################################################################################
@logger_cleaner
def plot_helper(_plt_handle, _title_text=None, _xlabel=None, _ylabel=None, _xticks=None, _yticks=None, _xlims=None,
                _ylims=None, _xlog_scale=False, _xticks_rotation=None, _ylog_scale=False, _xticklabel_size=None,
                _yticklabel_size=None, _yticks_rotation=None, _title_fontsize=10, _xlabel_fontsize=10,
                _ylabel_fontsize=10, _xlabel_fontweight='normal', _ylabel_fontweight='normal',
                _xticklabel_weight='normal', _yticklabel_weight='normal', _title_fontweight='normal',
                _xtick_labels=None, _ytick_labels=None, _xlabelpad=10, _ylabelpad=10, _legend_fontsize=10,
                _xticks_rotation_dic=None, _yticks_rotation_dic=None, _legend_fontweight='normal', **kwargs):

    logger_ = kwargs['logger']
    if _xlog_scale:
        _plt_handle.xscale('symlog')
    if _ylog_scale:
        _plt_handle.yscale('symlog')
    if _xticks is not None:
        logger_.info('Xticks are provided')
        if _xtick_labels is None and '_xtick_labels' in kwargs:
            _xtick_labels = kwargs['_xtick_labels']

        _plt_handle.xticks(
            _xticks,
            _xtick_labels,
        )
    if _xticks_rotation is not None:
        if _xticks_rotation_dic is None:
            _xticks_rotation_dic = {
                'rotation_mode': "anchor",
                'ha': "right"
            }
        _plt_handle.xticks(
            rotation=_xticks_rotation,
            rotation_mode=_xticks_rotation_dic['rotation_mode']
            if 'rotation_mode' in _xticks_rotation_dic else None,
            ha=_xticks_rotation_dic['ha']
            if 'ha' in _xticks_rotation_dic else None
        )
    if _xticklabel_size is not None:
        _plt_handle.xticks(
            size=_xticklabel_size,
            weight=_xticklabel_weight
        )
    if _yticks is not None:
        _plt_handle.yticks(
            _yticks,
            _ytick_labels
        )
    if _yticks_rotation is not None:
        if _yticks_rotation_dic is None:
            _yticks_rotation_dic = {
                'rotation_mode': "anchor",
                'ha': "right"
            }
        _plt_handle.yticks(
            rotation=_yticks_rotation,
            rotation_mode=_yticks_rotation_dic['rotation_mode']
            if 'rotation_mode' in _yticks_rotation_dic else None,
            ha=_yticks_rotation_dic['ha']
            if 'ha' in _yticks_rotation_dic else None
        )
    if _yticklabel_size is not None:
        _plt_handle.yticks(
            size=_yticklabel_size,
            weight=_yticklabel_weight
        )
    if _title_text is not None:
        _plt_handle.title(
            _title_text,
            fontsize=_title_fontsize,
            fontweight=_title_fontweight
        )
    if _xlabel is not None:
        _plt_handle.xlabel(
            _xlabel,
            fontsize=_xlabel_fontsize,
            fontweight=_xlabel_fontweight,
            labelpad=_xlabelpad
        )
    if _ylabel is not None:
        _plt_handle.ylabel(
            _ylabel,
            fontsize=_ylabel_fontsize,
            fontweight=_ylabel_fontweight,
            labelpad=_ylabelpad
        )
    if _xlims is not None:
        _plt_handle.xlim(_xlims)
    if _ylims is not None:
        _plt_handle.ylim(_ylims)

    legend_properties = {'weight': _legend_fontweight, 'size':_legend_fontsize}
    _plt_handle.legend(prop=legend_properties)

    if '_grid' in kwargs:
        _grid = kwargs['_grid']
        if _grid == 'on':
            plt.grid(color='#999999', linestyle=':', linewidth=0.7, axis='both')


# boxplot using pre-calculated statistics
# ######################################################################################################################
@logger_cleaner
def draw_stat_boxplot(_stats_dataframe, *args, _labels=None, _title_text=None, _save_address=None, _xlog_scale=None,
                      _xlabel=None, _ylabel=None, _different_group=None, _ylog_scale=None, _xticks=None, _yticks=None,
                      _first_group_color=None, _second_group_color=None, _xticks_rotation=None, _xticklabel_size=None,
                      _xlims=None, _ylims=None, _yticks_rotation=None, _yticklabel_size=None, _fig_size=None,
                      _whislo_negative=True, _sns_on=False, _plot_means=True, _title_fontsize=10, _xlabel_fontsize=10,
                      _ylabel_fontsize=10, _patch_facecolor=None, **kwargs):
    if _sns_on:
        sns.set()

    logger_ = kwargs['logger']
    columns = _stats_dataframe.columns
    N = _stats_dataframe.shape[1]
    _stats_dataframe.loc['whislo'] = \
        _stats_dataframe.loc['25%'] - 1.5 \
        * (_stats_dataframe.loc['75%']
           - _stats_dataframe.loc['25%'])
    _stats_dataframe.loc['whishi'] = \
        _stats_dataframe.loc['75%'] + 1.5 \
        * (_stats_dataframe.loc['75%']
           - _stats_dataframe.loc['25%'])
    if _whislo_negative is True:
        _stats_dataframe.loc['whislo',
                             _stats_dataframe.loc['whislo'] < 0] = 0

    stats = [{'label': columns[n],
              'q1': _stats_dataframe.loc['25%', columns[n]],
              'med': _stats_dataframe.loc['50%', columns[n]],
              'q3': _stats_dataframe.loc['75%', columns[n]],
              'whislo': _stats_dataframe.loc['whislo', columns[n]],
              'whishi': _stats_dataframe.loc['whishi', columns[n]],
              'fliers': []}
             for n in range(N)]

    if _labels is None:
        _labels = [stats[n]['label'] for n in range(len(stats))]
    if _different_group is None:
        _different_group = []
    if _first_group_color is None:
        _first_group_color = 'blue'
    if _second_group_color is None:
        _second_group_color = 'gold'

    if _fig_size is None:
        fig = plt.figure(figsize=(15, 10))
    else:
        fig = plt.figure(figsize=(_fig_size[0], _fig_size[1]))

    boxprops = dict(linestyle='-', linewidth=3)
    medianprops = dict(linestyle='-', linewidth=3, color='#000000')
    whiskerprops = dict(linestyle='-', linewidth=3)
    capprops = dict(linestyle='-', linewidth=3)

    axes = fig.add_subplot(1, 1, 1)
    bxps = axes.bxp(stats, boxprops=boxprops,
                    medianprops=medianprops,
                    whiskerprops=whiskerprops,
                    capprops=capprops,
                    patch_artist=True)
    axes.set_xticklabels(labels=_labels)
    for patch_no in range(len(bxps['boxes'])):
        patch = bxps['boxes'][patch_no]
        if _patch_facecolor is not None:
            patch.set_facecolor(_patch_facecolor[patch_no])
            patch.set_edgecolor(_patch_facecolor[patch_no])
        else:
            if _labels[patch_no] not in _different_group:
                plt.setp(patch, color=_first_group_color)
            else:
                plt.setp(patch, color=_second_group_color)

    plt.grid(color='#BBBBBB', linestyle=':', linewidth=0.8)
    plot_helper(plt, _title_text=_title_text, _xlabel=_xlabel, _ylabel=_ylabel, _xticks=_xticks, _yticks=_yticks,
                _xlims=_xlims, _ylims=_ylims, _xlog_scale=_xlog_scale, _xticks_rotation=_xticks_rotation,
                _ylog_scale=_ylog_scale, _xticklabel_size=_xticklabel_size, _yticklabel_size=_yticklabel_size,
                _yticks_rotation=_yticks_rotation, _title_fontsize=_title_fontsize, _xlabel_fontsize=_xlabel_fontsize,
                _ylabel_fontsize=_ylabel_fontsize, **kwargs)

    if _plot_means:
        means = _stats_dataframe.loc['mean']
        positions = range(1, _stats_dataframe.shape[1] + 1)
        if _patch_facecolor is not None:
            plt.scatter(
                positions,
                means,
                c=_patch_facecolor,
                edgecolors='#000000',
                marker='X',
                s=200,
                zorder=100
            )
        else:
            plt.scatter(
                positions,
                means,
                c='#ff0000',
                edgecolors='#000000',
                marker='X',
                s=200
            )

    if _save_address is not None:
        plt.savefig(_save_address, bbox_inches='tight')
        plt.close()
        logger_.info(f'Figure saved to {_save_address}.')
    else:
        if 'not_show_yet' not in args:
            plt.ion()
            plt.show()
        else:
            logger_.info('not showing yet !')


# ######################################################################################################################
@logger_cleaner
def plot_features_CDF(_df_list, _features_list, _file_list, _dataset_name, _save_folder=None, _xlog_scale=False,
                      _figsize=None, _linewidth=None, _legend_array=None, _xlim=None, _save_type=None, **kwargs):
    logger = kwargs['logger']
    if _figsize is None:
        _figsize = (15, 10)
    if _linewidth is None:
        _linewidth = 1

    if _save_type is None:
        _save_type = 'pdf'

    if _legend_array is None:
        _legend_array = []

    fig_dict = dict.fromkeys(_features_list)
    for n_df, df in enumerate(_df_list):
        file_name = _file_list[n_df]
        if not _legend_array:
            _legend_array.append(file_name)
        N = df.shape[0]
        Freq = np.array(range(N)) / float(N)
        # Freq = np.linspace(0, 1, n_top, endpoint=False)

        # fig_dict = dict.fromkeys(_features_list)
        for feature in _features_list:
            fig_dict[feature] = plt.figure(num=f'{feature}', figsize=_figsize)
            ax = fig_dict[feature].add_subplot(1, 1, 1)
            listed_col = df[f'{feature}'].to_list()
            listed_col.sort()
            ax.plot(listed_col, Freq, linewidth=_linewidth, color=dataset_colors[file_name])
            if _xlog_scale:
                plt.xscale('symlog')
            plt.xlabel(param_dic[feature]['xlabel'])
            plt.ylabel('Cumulative Frequency')
            plt.ylim([0, 1])
            plt.grid(color='#999999', linestyle=':', linewidth=0.7, axis='both')
            ax.tick_params(axis='x', labelsize=20)
            ax.tick_params(axis='y', labelsize=20)
            ax.set_xlabel(param_dic[feature]['xlabel'], fontsize=20)
            ax.set_ylabel('Cumulative Frequency', fontsize=20)
            if _xlim is not None:
                if _xlim.__class__ == dict:
                    ax.set_xlim(_xlim[feature])
                else:
                    ax.set_xlim(_xlim)
            logger.info(f'{feature} of {file_name} is plotted')

    for feature in _features_list:
        if _legend_array.__class__ == dict:
            fig_dict[feature].axes[0].legend(list(_legend_array.values()),
                                             fontsize=20, loc='right')
        else:
            fig_dict[feature].axes[0].legend(_legend_array,
                                             fontsize=20, loc='right')

    for feature in _features_list:
        if _save_folder is not None:
            save_name = os.path.join(_save_folder,
                                     ('log_scale_' if _xlog_scale else 'linear_') +
                                     feature + '.' + _save_type)
            fig_dict[feature].savefig(save_name, bbox_inches='tight')
            fig_dict[feature].clf()

    if _save_folder is None:
        plt.show()

    logger.info(f' All files of {_dataset_name} are done')


# error_bar using pre-calculated statistics
# ######################################################################################################################
@logger_cleaner
def draw_errorbar(_median_series, _std_series, _mean_series, _title_text=None, _save_address=None, _xlabel=None,
                  _different_group=None, _ylog_scale=False, _xticks=None, _yticks=None, _xticks_rotation=None,
                  _xticklabel_size=None, _xlims=None, _ylims=None, _yticks_rotation=None, _yticklabel_size=None,
                  _fig_size=None, _sns_on=False, _title_fontsize=10, _second_group_color='blue', _xlabel_fontsize=10,
                  _ylabel_fontsize=10, _xlabelpad=10, _ylabelpad=10, _xticks_rotation_dic=None,
                  _yticks_rotation_dic=None, **kwargs):
    mrkr_sz = 15
    if _sns_on:
        sns.set()

    logger_ = kwargs['logger']

    if 'labels' not in kwargs:
        labels = _median_series.index.to_list()
    else:
        labels = kwargs['labels']

    if 'ylabel' not in kwargs:
        ylabel = None
    else:
        ylabel = kwargs['ylabel']

    if _fig_size is None:
        fig = plt.figure(figsize=(15, 10))
    else:
        fig = plt.figure(figsize=(_fig_size[0], _fig_size[1]))

    median_stats = _median_series.to_list()
    std_stats = _std_series.to_list()
    mean_stats = _mean_series.to_list()
    x_vec = list(range(len(mean_stats)))

    axis = fig.add_subplot(1, 1, 1)
    axis.errorbar(
        x_vec,
        median_stats,
        yerr=[median_stats, std_stats],
        elinewidth=6,
        fmt='o',
        mec='#cccbbb',
        markerfacecolor='#ff0000',
        ms=mrkr_sz,
        color='#cccbbb'
    )
    axis.errorbar(
        x_vec,
        mean_stats,
        fmt='x',
        ms=mrkr_sz - 2,
        color='#ff0000'
    )
    axis.legend(['Median', 'Mean'], fontsize=22, loc="upper left")
    plt.setp(axis.xaxis.get_majorticklabels(), ha="right")

    if _different_group is not None:
        different_group_x = _different_group[0]
        different_group_median_stats = _different_group[1].to_list()
        different_group_std_stats = _different_group[2].to_list()
        different_group_mean_stats = _different_group[3].to_list()
        axis.errorbar(
            different_group_x,
            different_group_median_stats,
            yerr=[different_group_median_stats, different_group_std_stats],
            fmt='o',
            elinewidth=10,
            mec='#cccbbb',
            markerfacecolor='#ff0000',
            ms=mrkr_sz + 2,
            color=_second_group_color
        )
        axis.errorbar(
            different_group_x,
            different_group_mean_stats,
            fmt='x',
            ms=mrkr_sz,
            color='#ff0000'
        )

    if _ylog_scale:
        axis.set_yscale("log", nonpositive='clip')
    if _xticks is None:
        _xticks = x_vec
    axis.set_xticks(_xticks)
    axis.set_xticklabels(labels)

    plt.grid(color='#BBBBBB', linestyle=':', linewidth=0.8)
    plot_helper(plt, _title_text=_title_text, _xlabel=_xlabel, _ylabel=ylabel, _yticks=_yticks, _xlims=_xlims,
                _ylims=_ylims, _xticks_rotation=_xticks_rotation, _xticklabel_size=_xticklabel_size,
                _yticklabel_size=_yticklabel_size, _yticks_rotation=_yticks_rotation, _title_fontsize=_title_fontsize,
                _xlabel_fontsize=_xlabel_fontsize, _ylabel_fontsize=_ylabel_fontsize, _xlabelpad=_xlabelpad,
                _ylabelpad=_ylabelpad, _xticks_rotation_dic=_xticks_rotation_dic,
                _yticks_rotation_dic=_yticks_rotation_dic)

    if _save_address is not None:
        plt.savefig(_save_address, bbox_inches='tight')
        plt.close()
        logger_.info(f'Figure saved to {_save_address}.')
    else:
        plt.ion()
        plt.show()


# ######################################################################################################################
@logger_cleaner
def plot_two_bar(_x_data, _y_data, _xticks=None, _yticks=None, _nf_text=2, _hatches=None, _xticksl=None, _yticksl=None,
                 _colors=None, _save_address=None, _errors=None, _ylim=None, _xlabel=None, _ylabel=None, _legend=None,
                 _legend_loc=None, _title=None, **kwargs):
    logger_ = kwargs['logger']
    if _hatches is None:
        _hatches = ['---', 'xxx', '///', '...']
    if _colors is None:
        _colors = ['green', 'red']
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1, 1, 1)
    for num, x in enumerate(_y_data):
        ax.bar(_x_data[num], _y_data[num],
               linewidth=3,
               color='none',
               hatch=_hatches[num % 2],
               edgecolor=_colors[num % 2]
               )
        if _errors is not None:
            logger_.info("Errors is not None")
            ax.vlines(_x_data[num], _errors[0, num], _errors[1, num], label='_nolegend_',
                      linewidth=3, color=_colors[num % 2], capstyle='projecting')
            ax.hlines(_errors[0, num], _x_data[num] - 0.15, _x_data[num] + 0.15, label='_nolegend_',
                      linewidth=3, color=_colors[num % 2], capstyle='projecting')
            ax.hlines(_errors[1, num], _x_data[num] - 0.15, _x_data[num] + 0.15, label='_nolegend_',
                      linewidth=3, color=_colors[num % 2], capstyle='projecting')
        plt.text(
            _x_data[num] - 0.4,
            _y_data[num] + 0.001,
            f'{_y_data[num]:.{_nf_text}f}',
            fontsize=14,
            fontweight='bold'
        )
    if _title is not None:
        plt.title(_title, fontsize=14, fontweight='bold')
    if _xticks is not None:
        ax.set_xticks(_xticks)
    if _xticksl is not None:
        ax.set_xticklabels(_xticksl, fontweight='bold')
    if _ylim is not None:
        ax.set_ylim(_ylim)
    if _yticks is not None:
        ax.set_yticks(_yticks)
    if _yticks is not None:
        ax.set_yticklabels(_yticksl, fontweight='bold')
    if _xlabel is not None:
        plt.xlabel(_xlabel, fontsize=25, fontweight='bold')
    if _ylabel is not None:
        plt.ylabel(_ylabel, fontsize=25, fontweight='bold')
    ax.grid(axis='y', ls='-.', c='gray')
    ax.tick_params(axis='both', labelsize=20)
    legend_properties = {'weight': 'bold', 'size': 15}
    if _legend is not None:
        __ncol = 2
        if _legend_loc is None:
            _legend_loc = 'upper center'
        plt.legend(
            _legend,
            frameon=False,
            loc=_legend_loc,
            ncol=__ncol,
            # bbox_to_anchor=(1.1, 0.85),
            bbox_to_anchor=(0.45, 1.1),
            prop=legend_properties
        )
    if _save_address is None:
        plt.show()
    else:
        plt.savefig(_save_address, bbox_inches='tight')
        print(f'Barchart saved to {_save_address}')







# ~~~----~~~----~~~----~~~----~~~----~~~----~~~----~~~----~~~----~~~----~~~----~~~----~~~----~~~----~~~----~~~----~~~
@logger_cleaner
def plot_wasserstein_table(wasserstein_table, _labels, *args, _save_address=None, **kwargs):
    """
    This method assumes 5 elements in the given table (just for modifying shifts)
    :param wasserstein_table:
    :param _labels:
    :param _save_address: if provided, the plot will be saved this address
    :param kwargs:
    :return:
    """

    logger_ = kwargs['logger']

    if '_feature_name' in kwargs:
        _feature_name = kwargs['_feature_name']
    else:
        _feature_name = 'Not Given'

    if 'cbar_label' in kwargs:
        cbar_label = kwargs['cbar_label']
    elif '_feature_name' in kwargs:
        cbar_label = f'Wasserstein Distance ({_feature_name})'
    else:
        cbar_label = f'Wasserstein Distance'

    if '_figsize' in kwargs:
        _figsize = kwargs['_figsize']
    else:
        _figsize = (15, 12)
    fig = plt.figure(num=f'{_feature_name}', figsize=_figsize)
    if '_annot_fontsize' in kwargs:
        _annot_fontsize = kwargs['_annot_fontsize']
    else:
        _annot_fontsize = 15

    if 'cmap' in kwargs:
        cmap = kwargs['cmap']
    else:
        cmap = 'jet'

    if 'number_format' in kwargs:
        number_format = kwargs['number_format']
    else:
        number_format = "0.2f"

    if 'vmin' in kwargs:
        vmin = kwargs['vmin']
    else:
        vmin = wasserstein_table.min()
    if 'vmax' in kwargs:
        vmax = kwargs['vmax']
    else:
        vmax = wasserstein_table.max()
    ax = sns.heatmap(wasserstein_table,
                     vmin=vmin, vmax=vmax,
                     annot=True, annot_kws={"fontsize": _annot_fontsize},
                     cmap=cmap, cbar_kws={'label': cbar_label},
                     fmt=number_format)

    plot_helper(plt, **kwargs)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_xticklabels(_labels)
    ax.set_yticklabels(_labels)
    if 'bold_xticklabels' in args:
        [x.set_fontweight('bold') for x in ax.get_xticklabels()]
    if 'bold_yticklabels' in args:
        [x.set_fontweight('bold') for x in ax.get_yticklabels()]
    if '_xticklabel_size' in kwargs:
        _xticklabel_size = kwargs['_xticklabel_size']
    else:
        _xticklabel_size = 10
    ax.tick_params(axis='x', labelsize=_xticklabel_size)
    if '_yticklabel_size' in kwargs:
        _yticklabel_size = kwargs['_yticklabel_size']
    else:
        _yticklabel_size = 10
    ax.tick_params(axis='y', labelsize=_yticklabel_size)

    if '_cbar_ticklabel_fontsize' in kwargs:
        _cbar_ticklabel_fontsize = kwargs['_cbar_ticklabel_fontsize']
    else:
        _cbar_ticklabel_fontsize = 20
    ax.figure.axes[-1].tick_params(axis='y', labelsize=_cbar_ticklabel_fontsize)

    if '_cbar_label_fontsize' in kwargs:
        _cbar_label_fontsize = kwargs['_cbar_label_fontsize']
    else:
        _cbar_label_fontsize = 25
    ax.figure.axes[-1].yaxis.label.set_size(_cbar_label_fontsize)

    if 'bold_cbarlabels' in args:
        ax.figure.axes[-1].yaxis.label.set_weight('bold')
    plt.setp(ax.yaxis.get_majorticklabels())
    plt.tight_layout()


    # Shifting the yticks:
    dx = 0
    if 'y_shift' in kwargs:
        dy = kwargs['y_shift']
    elif wasserstein_table.shape[0] <= 5:
        dy = [10 / 72., 10 / 72., 35 / 72., 55 / 72., 30 / 72.]
    else:
        dy = [15 / 72., 15 / 72., 15 / 72., 15 / 72., 10 / 72., 35 / 72., 15 / 72., 15 / 72., 15 / 72.]

    for k, label in enumerate(ax.yaxis.get_majorticklabels()):
        offset = matplotlib.transforms.ScaledTranslation(dx, dy[k], fig.dpi_scale_trans)
        label.set_transform(label.get_transform() + offset)

    if _save_address is not None:
        plt.savefig(_save_address, bbox_inches='tight')
        logger_.info(f'Figure is saved to {_save_address}')
        plt.close()
    else:
        plt.show()









# ######################################################################################################################
@logger_cleaner
def plot_CDF_list(CDF_list, **kwargs):
    logger_ = kwargs['logger']
    if '_figsize' in kwargs:
        _figsize = kwargs['_figsize']
    else:
        _figsize = (10, 7)

    if '_line_colors' in kwargs:
        _line_colors = kwargs['_line_colors']
    else:
        _line_colors = random_hex_color(len(CDF_list))

    if '_legend_array' in kwargs:
        _legend_array = kwargs['_legend_array']
    else:
        _legend_array = None

    if '_linewidth' in kwargs:
        _linewidth = kwargs['_linewidth']
    else:
        _linewidth = 2

    for n, cdf in enumerate(CDF_list):
        sorted_values, Freq = cdf
        plt.plot(sorted_values, Freq,
                 color=_line_colors[n], linewidth=_linewidth,
                 label=_legend_array[n] if _legend_array is not None else None
                 )

    plt.legend(fontsize=20, loc='right')
    plot_helper(plt, **kwargs)

    if '_save_address' in kwargs:
        _save_address = kwargs['_save_address']
        plt.savefig(_save_address, bbox_inches='tight')
        logger_.info(f"List CDF plot is saved to: {_save_address}")
    else:
        plt.show()









# ######################################################################################################################
@logger_cleaner
def plot_hist_list(df_list, datasets_list, colors, *args, **kwargs):
    logger_ = kwargs['logger']
    if 'n_bins' in kwargs:
        n_bins = kwargs['n_bins']
    else:
        n_bins = 120
    for n, df in enumerate(df_list):
        if type(df) == pd.DataFrame:
            plt.hist(df.values, n_bins, facecolor='none', edgecolor=colors[n], label=datasets_list[n])
        else:
            plt.hist(df, n_bins, facecolor='none', edgecolor=colors[n], label=datasets_list[n])

    plt.legend()
    if 'log_scale' in args:
        plt.yscale('log')
    if 'title' in kwargs:
        title = kwargs['title']
        plt.title(title)

    if 'save_fldr' in kwargs:
        save_fldr = kwargs['save_fldr']
        if 'name_prefix' in kwargs:
            name_prefix = kwargs['name_prefix']
        else:
            name_prefix = ""
        save_name = f'hist_{"_".join(datasets_list)}{name_prefix}.pdf'
        save_path = os.path.join(save_fldr, save_name)
        plt.tight_layout()
        plt.savefig(save_path)
        logger_.info(f'the histogram is saved to {save_path}')

    plt.show()


# ######################################################################################################################
@logger_cleaner
def draw_list_boxplot(_lists, *args, _labels=None, _title_text=None, _save_address=None, _xlog_scale=None, _xlabel=None,
                      _ylabel=None, _different_group=None, _ylog_scale=None, _xticks=None, _yticks=None,
                      _colors=None, _xticks_rotation=None, _xticklabel_size=None, vertical=True,
                      _xlims=None, _ylims=None, _yticks_rotation=None, _yticklabel_size=None, _fig_size=None,
                      _title_fontsize=10, _xlabel_fontsize=10, _ylabel_fontsize=10, **kwargs):
    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_green,bg_yellow'

    logger_.info('plotting the boxplot ...')
    if _labels is None:
        _labels = list(range(len(_lists)))

    flier_props = dict(marker='x', markersize=3)
    median_props = dict(linewidth=1, color='red')
    if _fig_size is None:
        plt.figure(figsize=(15, 10))
    else:
        plt.figure(figsize=(_fig_size[0], _fig_size[1]))

    if 'rasterize' in args:
        plt.gca().set_rasterization_zorder(100)
    boxes = plt.boxplot(_lists, labels=_labels, vert=vertical, patch_artist=True,
                        flierprops=flier_props, medianprops=median_props)

    logger_.info('Customizing the patches in boxplot ...')
    if _colors is not None:
        for patch_no in range(len(boxes['boxes'])):
            patch = boxes['boxes'][patch_no]
            patch.set_facecolor(_colors[patch_no])

    plt.grid(color='#BBBBBB', linestyle=':', linewidth=0.8)
    plot_helper(plt, _title_text=_title_text, _xlabel=_xlabel, _ylabel=_ylabel, _xticks=_xticks, _yticks=_yticks,
                _xlims=_xlims, _ylims=_ylims, _xlog_scale=_xlog_scale, _xticks_rotation=_xticks_rotation,
                _ylog_scale=_ylog_scale, _xticklabel_size=_xticklabel_size, _yticklabel_size=_yticklabel_size,
                _yticks_rotation=_yticks_rotation, _title_fontsize=_title_fontsize, _xlabel_fontsize=_xlabel_fontsize,
                _ylabel_fontsize=_ylabel_fontsize)

    if _save_address is not None:
        if 'dpi' in kwargs:
            dpi = kwargs['dpi']
        else:
            dpi = 100
        plt.savefig(_save_address, bbox_inches='tight', dpi=dpi)
        plt.close()
        logger_.info(f'Figure saved to {_save_address}.')
    else:
        plt.ion()
        plt.show()




# ######################################################################################################################
@logger_cleaner
def save_my_figure(fig_handle, name_base, name_prefix, _save_fldr, _save_formats, plot_type, *args, **kwargs):

    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_green,bold'
    if not os.path.isdir(_save_fldr):
        os.mkdir(_save_fldr)
        logger_.info(f'The folder {_save_fldr} is created, it did not exist before.')

    feature_ = "_".join(name_base.split())
    _save_name = f'{name_prefix}-{plot_type}-{feature_.split(".")[0]}'
    save_address = os.path.join(_save_fldr, _save_name)
    if 'just_make_address' in args:
        return save_address+f'.{_save_formats[0]}'

    fig_handle.savefig(f'{save_address}.pdf', bbox_inches='tight')
    logger_.info(f'figure is saved to {save_address}.pdf')
    if len(_save_formats) > 1:
        dill.dump(fig_handle,
                  open(f'{save_address}.pickle', 'wb'), protocol=-1)
        logger_.info(f'figure is also saved in pickle to'
                     f' the {save_address}.pickle')
    plt.close(fig_handle)