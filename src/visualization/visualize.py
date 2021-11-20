import matplotlib.pyplot as plt

from src.data.io import get_info_df, show_info
from src.data.utils import create_info_subset
import cv2


def show_images(raw_data_path, all=False, file_names=None, n=None, rand=False, scaler=None, print_info=True,
                print_overview=True, matplot=True, label=None, hide_spines=False):
    """
    Functions print images with cv2.imshow.
    Note, matplotlib tends to not show full resolution, this is why it's usage is omitted here.

    Args:
        matplot: ust matplotlib to print (lower resultion but works within jupyter notebook)
        raw_data_path: absolut path to the raw data
        all: show all images
        file_names: how subset determined by file names
        n: show first n images if rand is false; else shows random n images
        rand: see n
        scaler: determines the value by which you want to up- or downsclae the img before it is shown
        print_info: use project specific info file/ function to print info for each file
        print_overview: print general information about the whole dataset
    """

    # Load info file or create one
    info = get_info_df(raw_data_path, overwrite_info=False)

    if print_info and print_overview:
        show_info(data_path=raw_data_path, file_names=file_names, n=n, rand=rand, overview=True, label=label)

    elif print_info and not print_overview:
        show_info(data_path=raw_data_path, file_names=file_names, n=n, rand=rand, overview=False, label=label)

    # Print all images
    subset_info = create_info_subset(info, all=all, file_names=file_names, rand=rand, label=label)

    for index, row in subset_info.iterrows():
        name = row['names'] + '.' + str(row['labels']) + '.jpg'
        show_image(raw_data_path=raw_data_path, name=name, label=row['labels'], scaler=scaler, hide_spines=hide_spines, matplot=matplot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_image(name, label=0,raw_data_path=None, scaler=None, gray=False, hide_spines=False, image=None, matplot=True):
    """
    Builtin-function used to print on image with corresponding headline.
    Args:
        raw_data_path: see show_images
        name: file name
        label: label in the format raw_dat/name.label.file_type specifies if the img is a fragment of a papyri.
        scaler:see show_images
    """
    if image is None:
        img = cv2.imread(raw_data_path + name, 1)
    else:
        img = image

    if scaler is None:
        if matplot:
            dpi = 80
            if gray:
                height, width = img.shape
            else:
                height, width, _ = img.shape

                # What size does the figure need to be in inches to fit the image?
            figsize = width / float(dpi), height / float(dpi)

            # Create a figure of the right size with one axes that takes up the full figure
            fig = plt.figure(figsize=figsize)
            ax = fig.add_axes([0, 0, 1, 1])

            # Hide spines, ticks, etc.
            # ax.axis('off')
            if hide_spines:
                ax.axis('off')
            else:
                ax.tick_params(axis='both', which='major', labelsize=40)
                ax.tick_params(axis='both', which='minor', labelsize=30)

            ax.set_title(f"original\n{name}", pad=30, fontsize=50)

            # Display the image.
            if gray:
                ax.imshow(img, cmap='gray')
            else:
                ax.imshow(img)
        else:
            cv2.imshow(f'{name}\nOriginal Size\n{label = }', img)

    else:
        img_scaled = cv2.resize(img, (0, 0), fx=scaler, fy=scaler)
        if scaler > 1:
            title_string = f'{name}\nUpscale by {(scaler - 1) * 100}%\n{label = }'
        else:
            title_string = f'{name}\nDownscaled by {(1 - scaler) * 100}%\n{label = }'
        if matplot:
            dpi = 120
            if gray:
                height, width = img_scaled.shape
            else:
                height, width, _ = img_scaled.shape

                # What size does the figure need to be in inches to fit the image?
            figsize = width / float(dpi), height / float(dpi)

            # Create a figure of the right size with one axes that takes up the full figure
            fig = plt.figure(figsize=figsize)
            ax = fig.add_axes([0, 0, 1, 1])

            # Hide spines, ticks, etc.
            # ax.axis('off')
            if hide_spines:
                ax.axis('off')
            else:
                ax.tick_params(axis='both', which='major', labelsize=40)
                ax.tick_params(axis='both', which='minor', labelsize=30)

            ax.set_title(title_string, pad=30, fontsize=50)

            # Display the image.
            if gray:
                ax.imshow(img_scaled, cmap='gray')
            else:
                ax.imshow(img_scaled)

        else:
            cv2.imshow(title_string, img_scaled)
