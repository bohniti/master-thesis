import streamlit as st
import pandas as pd
from PIL import Image


st.write('Papyri Inference APP')
val_path = '/Users/beantown/PycharmProjects/master-thesis/data/processed/05_val/'
df = pd.read_csv(val_path + 'processed_info.csv')
papyIDs = sorted(df.papyID.unique())

papyID = st.selectbox('Select PapyID', papyIDs)
fragmentIDs = sorted(df.loc[df['papyID'] == papyID].fragmentID.unique())
fragmentID = st.selectbox('Select PapyID', fragmentIDs)

# show Input image
input_fragments = df.loc[df['papyID'] == papyID]
input_img_path = val_path + input_fragments.loc[input_fragments['fragmentID']==fragmentID].fnames.values[0] + '.png'
image = Image.open(input_img_path)


st.image(image, caption=f'{fragmentID}th fragment of papyri with ID {papyID}')



