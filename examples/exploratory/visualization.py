from src.visualization.visualize import show_imgs

path = '/Users/beantown/PycharmProjects/master-thesis/data/raw/'

files = ['Bodleian-Library-MS-Gr-class-a-1-P-1-10_00001_frame-1',
              'Bodleian-Library-MS-Gr-class-a-8-P_00001_section-1-recto']

scale = 0.25

show_imgs(raw_data_path=path, n=5, rand=False, scaler=scale, print_info=True, print_overview=True)
show_imgs(raw_data_path=path, file_names=files, rand=False, scaler=scale, print_info=True, print_overview=True)