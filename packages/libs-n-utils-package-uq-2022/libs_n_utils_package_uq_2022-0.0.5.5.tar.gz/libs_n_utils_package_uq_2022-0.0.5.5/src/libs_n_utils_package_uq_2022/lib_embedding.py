import os
import feather
import umap
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, LocallyLinearEmbedding, MDS, SpectralEmbedding
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.impute import SimpleImputer
import numpy as np
from . import config_template
from .lib_feature_calculation import features_calculation
from .my_easy_logger import logger_cleaner
import matplotpyplot as plt

script_name = os.path.split(__file__)[1]
groupby_features = config_template.features.groupby_features
features_class = config_template.features()
ds_colors = config_template.plot_parameters.dataset_edgecolors
ds_short_names = config_template.plot_parameters.dataset_shorts
ds_markers = config_template.plot_parameters.dataset_markers
ds_facecolors = config_template.plot_parameters.dataset_facecolors
func_color = 'black'


# ##############################################################################################################
@logger_cleaner
def embedding_data_prepare(datasets_list_, df_type_, selected_fields_,features_list_,
                           base_save_folder_, coms_sel_sets_,sample_size_, fields_,
                           mother_folder=None, save_csv=True, seed=0, size_log=True, **kwargs):
    logger_ = kwargs['logger']
    logger_.setLevel(10)
    if mother_folder is None:
        mother_folder = '/storage/datasets'
    features_list_ = [x for x in features_list_ if x not in groupby_features]
    logger_.info('Embeddings are calculated only over non-group-by features.\n'
                 'Because group-by features are not one-to-one, '
                 'so their number is much smaller than samples')

    overall_df = pd.DataFrame()
    for dataset in datasets_list_:
        logger_.info(f'Reading dataset {dataset} \n{"*" * 200}')
        dataset_folder = f'{mother_folder}/{dataset}/{df_type_}'

        file_list = os.listdir(dataset_folder)
        file_list.sort()
        df_ = pd.DataFrame()
        for file_name in file_list:
            if (dataset == 'Comscentre2017') and (file_name not in coms_sel_sets_):
                logger_.setLevel(10)
                logger_.debug(f'{file_name} was not loaded')
                continue
            file_address = os.path.join(dataset_folder, file_name)
            logger_.info(f'Reading file {file_name} ...')
            df = feather.read_dataframe(file_address, columns=selected_fields_)
            df = df.sample(n=sample_size_, replace=False, random_state=seed)
            df.reset_index(drop=True, inplace=True)
            logger_.info('Calculating features...')
            df = features_calculation(df, features_list_, _unidirect_flow=False)
            df = df[features_list_]
            x = MinMaxScaler().fit_transform(df)
            df = pd.DataFrame(x, columns=features_list_)
            df_ = df_.append(df, ignore_index=True)

        df_['dataset_name'] = dataset
        logger_.info(f'All features from "{dataset}" '
                     f'are extracted and saved.')
        overall_df = overall_df.append(df_, ignore_index=True)

    if save_csv is True:
        csv_file_name = os.path.join(base_save_folder_,
                                     f'ngbfeatures_{sample_size_}_{"-".join(datasets_list_)}_seed_{seed}.csv')
        overall_df.to_csv(csv_file_name, index=False)
        logger_.info(f'All non-groupby features of {datasets_list_} are saved to {csv_file_name}')

    # Applying standardization and then handling NaNs for PCA
    # x = overall_df.loc[:, features_list_].values
    # x = StandardScaler().fit_transform(x)
    # x = MinMaxScaler().fit_transform(x)
    # y_ = overall_df.loc[:, ['dataset_name']].values
    # imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
    # imp_mean.fit(y_)
    # all_dataset_scaled = imp_mean.transform(x)

    return overall_df





# ###################################################################################################################
@logger_cleaner
def compute_embeddings(all_datasets, embedding_func='pca', n_neighbors=3, random_seed=0, **kwargs):
    logger_ = kwargs['logger']

    if embedding_func == 'umap':
        embedder = umap.UMAP(
            n_components=2,
            random_state=random_seed
        )
    # elif embedding_func == 'tsne':
    #     embedder = TSNE(
    #         n_components=2,
    #         init='pca',
    #         random_state=random_seed,
    #         perplexity=3000
    #     )
    elif embedding_func == 'tsne':
        embedder = TSNE(
            n_components=2,
            random_state=random_seed
        )
    elif embedding_func == 'lda':
        embedder = LinearDiscriminantAnalysis(
            n_components=2
        )
    elif embedding_func == 'llem':
        embedder = LocallyLinearEmbedding(
            n_neighbors=n_neighbors,
            n_components=2,
            eigen_solver='dense',
            method='modified'
        )
    elif embedding_func == 'lle':
        embedder = LocallyLinearEmbedding(
            n_neighbors=n_neighbors,
            n_components=2,
            random_state=random_seed,
            eigen_solver='dense',
            method='hessian'
        )
    elif embedding_func == 'mds':
        embedder = MDS(
            n_components=2,
            random_state=random_seed,
            n_init=1,
            max_iter=100
        )
    elif embedding_func == 'spec':
        embedder = SpectralEmbedding(
            n_components=2,
            random_state=random_seed,
            eigen_solver="arpack"
        )
    else:
        embedder = PCA(
            n_components=2,
            random_state=random_seed
        )

    logger_.info(f'fitting the {embedding_func} to samples of all datasets')
    Y = all_datasets.pop('dataset_name').values
    all_datasets = all_datasets.values
    if embedding_func == 'lda':
        # all_datasets.flat[::all_datasets.shape[1] + 1] += 0.01
        embedding_ = embedder.fit(all_datasets, Y).transform(all_datasets)
    else:
        embedding_ = embedder.fit_transform(all_datasets)

    embedding_df = pd.DataFrame(
        data=embedding_,
        columns=['component 1',
                 'component 2']
    )
    embedding_df['dataset_name'] = Y

    return embedding_df


# ###################################################################################################################
@logger_cleaner
def plot_embeddings(all_dataset_embedding, datasets_list_, embedding_func, sample_size, *args, **kwargs):
    logger_ = kwargs['logger']
    # Plotting
    logger_.info(f'Lets plot the scatter plots for {embedding_func}')
    colors = [ds_colors[x] for x in datasets_list_]
    legend_names_ = [ds_short_names[x] for x in datasets_list_]
    markers = [ds_markers[x] for x in datasets_list_]
    facecolors = [ds_facecolors[x] for x in datasets_list_]
    linewidths = [0.5, 0.2, 0.1, 0.05, 0.05]

    fig = plt.figure(num=f'embedding_9features', figsize=(12, 10))
    ax = fig.add_subplot(1, 1, 1)
    if embedding_func == 'pca':
        xlabel = 'Principal Component 1'
        ylabel = 'Principal Component 2'
    else:
        xlabel = 'Embedded Component 1'
        ylabel = 'Embedded Component 2'
    ax.set_xlabel(xlabel, fontsize=20)
    ax.set_ylabel(ylabel, fontsize=20)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    for n, dataset in enumerate(datasets_list_):
        indicesToKeep = all_dataset_embedding['dataset_name'] == dataset
        ax.scatter(all_dataset_embedding.loc[indicesToKeep, 'component 1'],
                   all_dataset_embedding.loc[indicesToKeep, 'component 2'],
                   linewidths=linewidths[n], marker=markers[n],
                   facecolor=facecolors[n], edgecolor=colors[n],
                   rasterized=True)

    if 'set_title' in args:
        plt.title(f'Embeddings for {embedding_func}')

    # # just for spectral embeddings we need this
    # yticks = ax.get_yticks()
    # yticklabels = [f'{int(10000 * x)}' for x in yticks]
    # xticks = ax.get_xticks()
    # xticklabels = [f'{int(10000 * x)}' for x in xticks]
    # ax.set_xticklabels(xticklabels)
    # ax.set_yticklabels(yticklabels)

    line_list = []
    for n in range(len(datasets_list_)):
        line_list.append(plt.scatter([], [], s=60, facecolors=facecolors[n],
                         edgecolors=colors[n], marker=markers[n]))

    ax.legend(line_list, legend_names_,
              fontsize=20, loc='upper center',
              bbox_to_anchor=(.50, 1.18), ncol=3)

    if 'base_save_folder' in kwargs:
        base_save_folder_ = kwargs['base_save_folder']
        save_name = f'{embedding_func}_{"-".join(datasets_list_)}_{sample_size}samples.pdf'
        save_address = os.path.join(base_save_folder_, save_name)
        plt.savefig(save_address, bbox_inches='tight')
        logger_.info(f'figure is saved to {save_address}')
        plt.show()
        # plt.close(fig=fig)
    else:
        plt.show()

    logger_.info(f'{embedding_func} is now plotted !')
