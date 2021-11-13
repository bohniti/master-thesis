from src.features.build_features import create_patches_from_imgs
from src.visualization.visualize import show_images

raw_data_path = '/Users/beantown/PycharmProjects/master-thesis/data/raw/'
processed_data_path = '/Users/beantown/PycharmProjects/master-thesis/data/processed/'

files = ['Bodleian-Library-MS-Gr-class-a-1-P-1-10_00001_frame-1',
         'Bodleian-Library-MS-Gr-class-a-8-P_00001_section-1-recto']

scale = 0.25

create_patches_from_imgs(input_path=raw_data_path, output_path=processed_data_path, n=4)
show_images(raw_data_path=processed_data_path + '16_patches/', file_names=[files[0]], rand=False, scale=scale,
            print_info=True, print_overview=True)
