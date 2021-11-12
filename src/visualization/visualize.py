from src.data.io import get_info_df, show_info
import cv2


def show_images(raw_data_path, all=False, file_names=None, n=None, rand=False, scale=None, print_info=True,
                print_overview=True):
    """
    Functions print images with cv2.imshow.
    Note, matplotlib tends to not show full resolution, this is why it's usage is omitted here.

    Args:
        raw_data_path: absolut path to the raw data
        all: show all images
        file_names: how subset determined by file names
        n: show first n images if rand is false; else shows random n images
        rand: see n
        scale: determines the value by which you want to up- or downsclae the img before it is shown
        print_info: use project specific info file/ function to print info for each file
        print_overview: print general information about the whole dataset
    """

    def show_image(raw_data_path, name, label=0, scaler=None):
        """
        Builtin-function used to print on image with corresponding headline.
        Args:
            raw_data_path: see show_images
            name: file name
            label: label in the format raw_dat/name.label.file_type specifies if the img is a fragment of a papyri.
            scaler:see show_images
        """
        img = cv2.imread(raw_data_path + name, 1)
        if scaler is None:
            cv2.imshow(f'{name}\nOriginal Size\n{label = }', img)

        else:
            img_scaled = cv2.resize(img, (0, 0), fx=scaler, fy=scaler)
            if scaler > 1:
                title_string = f'{name}\nUpscale by {(scaler - 1) * 100}%\n{label = }'
            else:
                title_string = f'{name}\nDownscaled by {(1 - scaler) * 100}%\n{label = }'
            cv2.imshow(title_string, img_scaled)

    # Load info file or create one
    info = get_info_df(raw_data_path)

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
        show_image(raw_data_path=raw_data_path, name=name, label=row['labels'], scaler=scale)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



