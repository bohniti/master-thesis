from efficientnet_pytorch import EfficientNet
from PyPDF2 import PdfFileMerger
from shutil import copyfile
from fpdf import FPDF
import logging
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from pytorch_metric_learning import distances, losses, miners, reducers, testers
from pytorch_metric_learning.utils.accuracy_calculator import AccuracyCalculator
import pandas as pd
import PIL
import os
import toml
from os.path import isfile, join
from google.colab import drive
import matplotlib
from matplotlib import rc
import umap
import torch
import torchvision
from torchvision import datasets, transforms
from pytorch_metric_learning.testers import GlobalEmbeddingSpaceTester
from pytorch_metric_learning.utils import common_functions as c_f
from pytorch_metric_learning.utils.inference import InferenceModel, MatchFinder
import numpy as np
import cv2
from matplotlib import pyplot as plt