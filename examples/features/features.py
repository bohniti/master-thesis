from src.features.build_features import create_patches_from_imgs, retrieve_from_patches
from src.visualization.visualize import show_images
from src.data.io import get_images

raw_data_path = '/Users/beantown/PycharmProjects/master-thesis/data/raw/'

files = ['Bodleian-Library-MS-Gr-class-a-1-P-1-10_00001_frame-1_edges_x',
         'Bodleian-Library-MS-Gr-class-a-1-P-1-10_00001_frame-1_edges_y']

scale = 0.25

create_patches_from_imgs(input_path=raw_data_path,
                         output_path='/Users/beantown/PycharmProjects/master-thesis/data/processed/',
                         n=4,
                         gradients=True)

info = show_images(raw_data_path='/Users/beantown/PycharmProjects/master-thesis/data/processed/8_gradient_patches/',
                   all=False,
                   file_names=files,
                   rand=False,
                   scaler=scale,
                   print_info=True,
                   print_overview=False,
                   matplot=True,
                   label=1)

images = get_images(raw_data_path='/Users/beantown/PycharmProjects/master-thesis/data/processed/8_gradient_patches/',
                    file_names=files,
                    rand=False,
                    scaler=scale,
                    print_info=False,
                    print_overview=False,
                    label=1)

print(len(images))
