from archiv.io import show_info
from archiv.utils import create_info_subset
from src.features.externals.laplace import laplace
import cv2
import numpy as np
from pathlib import Path


def create_patches_from_imgs(input_path, output_path, all=False, names=None, patch_size=None, n=None, gradients=True,
                             laplacian=False):
    """
    Function creates a set of patches for given images.

    Args:
        input_path: path to a directory where images are hold
        output_path: path where img patches are saved
        all: if every image in input_path should be splitted
        names: just create splits for the specified img-names
        patch_size: NOT supported yet!
        n: the image will be spliced along axis n/2 times and than each split will be spliced again along axis 0
        gradients: if true compute and save edges in y and x direction
    """

    def create_patches_from_img(input, name, output_path, patch_size=None, n=None, gradient=True, laplacian=False):
        """
        Built-in function which splits an image first along x than along y axsis

        Args:
            input: see create_patches_from_imgs
            name: name of the original image determined by create_patches_from_imgs function
            output_path: see create_patches_from_imgs
            patch_size: see create_patches_from_imgs
            n: see create_patches_from_img
            gradient: if true compute and save edges in y and x direction
        """
        processed_info = show_info(data_path=output_path, overview=False, overwrite_info=True)

        if processed_info.empty or not any(processed_info['names'].str.contains(name)):

            path = input + name + '.0' + '.jpg'
            img = cv2.imread(path, 1)
            if n is not None:

                print(f'Split {name} into {n} equally sized patches')
                result = []
                imgs_axis_1 = np.array_split(img, n, axis=1)

                for img in imgs_axis_1:
                    result.append(np.array_split(img, n, axis=0))
                imgs = [item for sublist in result for item in sublist]

            if gradient:
                for label, img in enumerate(imgs):
                    kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
                    kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
                    edges_x = cv2.filter2D(img, cv2.CV_8U, kernelx)
                    edges_y = cv2.filter2D(img, cv2.CV_8U, kernely)
                    cv2.imwrite(output_path + name + '_edges_x.' + str(label) + '.jpg', edges_x)
                    cv2.imwrite(output_path + name + '_edges_y.' + str(label) + '.jpg', edges_y)
            elif laplacian:
                for label, img in enumerate(imgs):
                    laplace_img = laplace(img)
                    cv2.imwrite(output_path + name + '.' + str(label) + '.jpg', laplace_img)
            else:
                for label, img in enumerate(imgs):
                    cv2.imwrite(output_path + name + '.' + str(label) + '.jpg', img)
            print(f'Saved all patches of {name} successfully.')

            _ = show_info(data_path=output_path, overwrite_info=True, overview=False)

    # TODO Add feature patch_size if necessary. If not delete variable or error message.
    if n < 4:
        raise Exception('N values < 4 not supported yet')
    if not n % 2 == 0:
        raise Exception('Non equal numbers along each side are not allowed')

    if gradients:
        full_processed_data_path = output_path + f'/{int(n * 2)}_gradient_patches/'
        Path(full_processed_data_path).mkdir(parents=True, exist_ok=True)
    elif laplacian:
        full_processed_data_path = output_path + f'/{int(n * 2)}_laplace_patches/'
        Path(full_processed_data_path).mkdir(parents=True, exist_ok=True)
    else:
        full_processed_data_path = output_path + f'/{int(n * 2)}_patches/'
        Path(full_processed_data_path).mkdir(parents=True, exist_ok=True)

    n = n / 2

    if all:
        info = show_info(input_path, overview=False)
        names = info.names.tolist()
        print(names)
    elif names is not None:
        info = show_info(input_path, overview=False)
        subset_info = create_info_subset(info, all=False, file_names=names, rand=False)
        names = subset_info.names.tolist()

    for name in names:
        create_patches_from_img(input=input_path, name=name, output_path=full_processed_data_path,
                                patch_size=patch_size, n=n, gradient=gradients, laplacian=laplacian)
    _ = show_info(data_path=full_processed_data_path, overwrite_info=True, overview=False)


def retrieve_from_patches(input_path, output_path, name):
    info = show_info(data_path=input_path, file_names=[name])
    imgs = []
    subset_info = info[info['names'].isin([name])]
    patches_idx_vertical = subset_info['labels'].max()
    patches_count = subset_info['labels'].max() + 1

    full_processed_data_path = output_path + f'/retrieved_from_{patches_count}_patches/'
    Path(full_processed_data_path).mkdir(parents=True, exist_ok=True)

    for index, row in subset_info.iterrows():
        name = row['names'] + '.' + str(row['labels']) + '.jpg'
        img = cv2.imread(input_path + name, 1)
        imgs.append(img)

    patches_count_vertical = int(np.sqrt(patches_count))

    vertical_stacks = []

    for i in range(0, patches_count_vertical):
        to_stack = []
        for i in range(0, patches_count_vertical):
            to_stack.append(imgs.pop(0))
        to_stack = np.array(to_stack)
        stacked = np.vstack(to_stack)
        # print(stacked.shape)
        vertical_stacks.append(stacked)

    print(len(vertical_stacks))
    img = np.column_stack(np.array(vertical_stacks))
    # img = np.column_stack(img)
    print(img.shape)
