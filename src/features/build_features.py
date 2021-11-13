from src.data.io import get_info_df, show_info
import cv2
import numpy as np
from pathlib import Path


def create_patches(input_path, output_path, all=False, names=None, patch_size=None, n=None):


    if n < 4:
        raise Exception('N values < 4 not supported yet')
    if not n % 2 == 0:
        raise Exception('Non equal numbers along each side are not allowed')

    full_processed_data_path = output_path + f'/{int(n*2)}_patches/'
    Path(full_processed_data_path).mkdir(parents=True, exist_ok=True)

    n = n/2

    if all or names is None:
        info = show_info(input_path, overview=False)
        names = info.names.tolist()
        print(names)

    for name in names:
        create_patch(input_path=input_path, name=name, output_path=full_processed_data_path, patch_size=patch_size, n=n)
    _ = show_info(data_path=full_processed_data_path, overwrite_info=True, overview=False)


def create_patch(input_path, name, output_path, patch_size=None, n=None):
    processed_info = show_info(data_path=output_path, overview=False, overwrite_info=True)

    if processed_info.empty or not any(processed_info['names'].str.contains(name)):

        path = input_path + name + '.0' + '.jpg'
        img = cv2.imread(path, 1)
        if n is not None:

            print(f'Split {name} into {n} equally sized patches')
            result = []
            imgs_axis_1 = np.array_split(img, n, axis=1)

            for img in imgs_axis_1:
                result.append(np.array_split(img, n, axis=0))
            imgs = [item for sublist in result for item in sublist]

        for label, img in enumerate(imgs):
            cv2.imwrite(output_path + name + '.' + str(label) + '.jpg', img)
        print(f'Saved all patches of {name} successfully.')

        _ = show_info(data_path=output_path, overwrite_info=True, overview=False)
