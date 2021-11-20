import cv2
import matplotlib.pyplot as plt
from src.features.build_features import create_patches_from_imgs, retrieve_from_patches
from src.visualization.visualize import show_images, show_image
from src.data.io import get_images
import cv2 as cv

raw_data_path = '/Users/beantown/PycharmProjects/master-thesis/data/raw/michigan_data/data/'
matplot = False
scale = 0.25
files = ['1203_C1_11R', '1203_C1_11V', '1257_C2_7R', '1257_C2_7V']

show_images(raw_data_path=raw_data_path, file_names=files, rand=False, scaler=scale, print_info=True,
            print_overview=True)

files = ['1203_C1_11R_edges_x', '1203_C1_11R_edges_y']

if False:
    info = show_images(
        raw_data_path='/Users/beantown/PycharmProjects/master-thesis/data/processed/michigan/16_gradient_patches/',
        all=False,
        file_names=files,
        rand=False,
        print_info=True,
        print_overview=False,
        matplot=matplot,
        label=4,
        hide_spines=True)

patched_images = get_images(
    raw_data_path='/Users/beantown/PycharmProjects/master-thesis/data/processed/michigan/16_gradient_patches/',
    file_names=files,
    rand=False,
    print_info=False,
    print_overview=False,
    label=4)

img = patched_images[0]
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

orb = cv.ORB()

# find the keypoints with ORB
kp = orb.detect(img,None)


