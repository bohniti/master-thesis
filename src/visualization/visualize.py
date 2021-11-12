from src.data.io import get_info, show_info
import cv2

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






