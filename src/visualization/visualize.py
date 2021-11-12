from pathlib import Path
from PIL import Image
import numpy as np
from tabulate import tabulate
import pandas as pd
import cv2


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


def show_imgs(raw_data_path, all=False, file_names=None, n=None, rand=False, scaler=None, print_info=True,
              print_overview=True):
    # Load info file or create one
    info = get_info(raw_data_path)

    if print_info and print_overview:
        show_info(raw_data_path=raw_data_path, file_names=file_names, n=n, rand=rand, overview=True)

    elif print_info and not print_overview:
        show_info(raw_data_path=raw_data_path, file_names=file_names, n=n, rand=rand, overview=False)

    # Print all images
    if all:
       subset_info = info
    # Print subset of images given by filenames
    elif file_names is not None:
        subset_info = info[info['names'].isin(file_names)]
    # Print first n images
    elif n is not None and not rand:
        subset_info = info.head(n)
    # Print n random images
    elif n is not None and rand:
        subset_info = info.sample(n)

    for index, row in subset_info.iterrows():
        name = row['names'] + '.' + str(row['labels']) + '.jpg'
        show_img(raw_data_path=raw_data_path, name=name, label=row['labels'], scaler=scaler)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_img(raw_data_path, name, label=0, scaler=None):
    img = cv2.imread(raw_data_path + name, 1)
    if scaler is None:
        cv2.imshow(f'{name}\nOriginal Size\n{label = }', img)

    else:
        img_scaled = cv2.resize(img, (0, 0), fx=scaler, fy=scaler)
        if scaler > 1:
            title_string = f'{name}\nUpscaled by {(scaler - 1) * 100}%\n{label = }'
        else:
            title_string = f'{name}\nDownscaled by {(1 - scaler) * 100}%\n{label = }'
        cv2.imshow(title_string, img_scaled)






