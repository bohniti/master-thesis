from pathlib import Path
from PIL import Image
import numpy as np
from tabulate import tabulate
import pandas as pd


def get_info_df(raw_data_path, n=None):
    """
    Function reads or creates a .csv file in given dir.
    The file is for creating a pandas.DataFrame out of it.
    The dataframe contains the name, width, height and the label of each image in a given dir.

    Args
        raw_data_path: absolut path to the raw data
        n: use n if you want to create df just for first n! Not recommended!!!

    Returns
        pandas.DataFrame: info df can be used to read and write data and to calculate naive statistics.
    """

    info_file = Path(raw_data_path + 'info_file.csv')

    if info_file.is_file():
        print(f'\nRead info from {str(info_file)} ...')
        info = pd.read_csv(raw_data_path + 'info_file.csv')
        return info

    else:
        print(f'No info file found. Start collecting info from {raw_data_path} ...')
        p = Path(raw_data_path).glob('**/*.jpg')
        files = np.array([x for x in p if x.is_file()])
        heights = []
        widths = []
        names = []
        labels = []

        for file in files:
            im = Image.open(file)
            width, height = im.size
            heights.append(height)
            widths.append(width)
            file_splits = str(file).split('/')[-1]
            file_splits = str(file_splits).split('.')
            names.append(file_splits[0])
            labels.append(int(file_splits[1]))

        info = pd.DataFrame()
        info['names'] = names
        info['widths'] = widths
        info['heights'] = heights
        info['labels'] = labels

        print(f'Write info to info_file.csv')
        info.to_csv(raw_data_path + 'info_file.csv')
        return info


def show_info(raw_data_path, overview=True, file_names=None, n=None, rand=False):
    """
    Function uses the an project specific pandas df given by a info.csv file to print img or dataset information.
    Note,Just use filenames or n and rand parameters. File_names creats a subset out of the specified files.

    Args
        raw_data_path: path to data (.csv file)
        overview: if functions calculates and print naive statistics about the dataset
        file_names: if function prints sample-specific information
        n: prints n file-information strings
        rand: if true n doesn't print the first but instead random sample-information
    """
    info = get_info_df(raw_data_path=raw_data_path)
    if overview:
        nr_of_samples = info.shape[0]
        nr_of_labels = str(info['labels'].value_counts())
        max_width = info['widths'].max()
        max_height = info['heights'].max()
        median_width = info['widths'].median()
        median_height = info['heights'].median()
        mean_width = info['widths'].mean()
        mean_height = info['heights'].mean()
        print(
            f'\n\033[1mDataset Overview\033[0m\n'
            f'\n{  nr_of_samples = }'
            f'\n{  nr_of_labels = }'
            f'\n{  max_width = }'
            f'\n{  max_height = }'
            f'\n{  median_width = }'
            f'\n{  median_height = }'
            f'\n{  mean_width = }'
            f'\n{  mean_height = }\n')

    if file_names is not None:
        subset_info = info[info['names'].isin(file_names)]

        print(
            f'\n\033[1mFile Info\033[0m\n\n' + tabulate(subset_info, headers='keys', tablefmt='github',
                                                        showindex=False))
    elif n is not None and not rand:
        subset_info = info.head(n)
        print('\n\033[1mFile Info\033[0m\n\n' + tabulate(subset_info, headers='keys', tablefmt='github',
                                                         showindex=False))
    elif n is not None and rand:
        subset_info = info.sample(n)
        print('\n\033[1mFile Info\033[0m\n\n' + tabulate(subset_info, headers='keys', tablefmt='github',
                                                         showindex=False))