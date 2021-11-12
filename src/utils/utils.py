from pathlib import Path
from PIL import Image
import numpy as np
from tabulate import tabulate
import pandas as pd


def get_info(raw_data_path, n=None):
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
    info = get_info(raw_data_path=raw_data_path)
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


def show_imgs(raw_data_path, all=False, file_names=None, n=None, rand=False, scale=None):
    pass


def show_img(**kwargs):
    pass


def create_patches(**kwargs):
    pass


def create_patch(**kwargs):
    pass


show_info(raw_data_path='/Users/beantown/PycharmProjects/master-thesis/data/raw/', overview=True,
          n=10)
