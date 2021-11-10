from pathlib import Path
from PIL import Image
import numpy as np
import h5py


def get_info(raw_data_path, n=None):
    # TODO you have to exectue it twice as long as h5 file is created -> fix
    info_file = Path(raw_data_path + 'info_file.h5')

    if info_file.is_file():
        print(f'\nRead info from {str(info_file)} ...')

        with h5py.File(str(info_file), "r") as f:

            widths = np.array(f['widths']).flatten()
            heights = np.array(f['heights']).flatten()
            names = np.array(f['names']).flatten()
            labels = np.array(f['labels']).flatten()
        result = np.vstack((names, widths))
        result = np.vstack((result, heights))
        result = np.vstack((result, labels))
        return result


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

        heights = np.array(heights)
        widths = np.array(widths)


        dt = h5py.string_dtype(encoding='utf-8')

        with h5py.File(raw_data_path + 'info_file.h5', 'w') as h5f:
            h5f.create_dataset('names', data=names, dtype=dt)
            h5f.create_dataset('heights', data=heights)
            h5f.create_dataset('widths', data=widths)
            h5f.create_dataset('labels', data=labels)

        print(f'Write info to info_file.h5')
        get_info(raw_data_path=raw_data_path, n=n)


def show_info(raw_data_path, overview=True):
    info = get_info(raw_data_path=raw_data_path)
    if overview:
        nr_of_samples = info.shape[1]
        nr_of_labels = np.unique(info[3]).shape[0]
        max_width = info[2].max()
        max_height = info[1].max()
        median_width = np.median(info[2])
        median_height = np.median(info[1])
        mean_width = info[2].mean()
        mean_height = info[1].mean()
        print(
            f'\nDataset Overview:\n{  nr_of_samples = }\n{  nr_of_labels = }'
            f'\n{  max_width = }\n{  max_height = }\n{  median_width = }\n{  median_height = }\n{  mean_width = }\n{  mean_height = }')


def show_imgs(**kwargs):
    pass


def show_img(**kwargs):
    pass


def create_patches(**kwargs):
    pass


def create_patch(**kwargs):
    pass


show_info(raw_data_path='/Users/beantown/PycharmProjects/master-thesis/data/raw/')
