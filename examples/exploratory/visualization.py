# This example creates a dataset-specific information file if it does not exist,
# shows general information about the dataset and some file-specific information for some example images.

from src.visualization.visualize import show_images

path = '/Users/beantown/PycharmProjects/master-thesis/data/raw/'

files = ['Bodleian-Library-MS-Gr-class-a-1-P-1-10_00001_frame-1',
              'Bodleian-Library-MS-Gr-class-a-8-P_00001_section-1-recto']

scale = 0.25

show_images(raw_data_path=path, file_names=files, rand=False, scale=scale, print_info=True, print_overview=True)