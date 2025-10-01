# app/streamlit_grid.py
import streamlit as st
from PIL import Image
from pathlib import Path
import joblib, numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
import os

st.set_page_config(layout="wide", page_title="Plant Grid MVP")

MODEL_CLF = "models/clf.joblib"
DATA_DIR = Path("data/images")
classes = ["healthy","diseased"]

# Carregar classifier
clf = joblib.load(MODEL_CLF)

# Carregar embedder (same as training)
embedder = MobileNetV2(weights="imagenet", include_top=False, pooling="avg", input_shape=(224,224,3))

def predict_image(p):
    img = image.load_img(p, target_size=(224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x,0)
    x = preprocess_input(x)
    emb = embedder.predict(x, verbose=0)
    pred = clf.predict(emb)[0]
    proba = clf.predict_proba(emb).max()
    return pred, float(proba)

st.title("MVP — Grid de plantas")
col1, col2 = st.columns([3,1])

# Sidebar
with col2:
    st.header("Controls")
    n_cols = st.slider("Columns", 1, 6, 3)
    source = st.selectbox("Source folder", [d.name for d in DATA_DIR.iterdir() if d.is_dir()])

# List images
img_folder = DATA_DIR / source
image_paths = [p for p in img_folder.glob("*") if p.suffix.lower() in [".jpg",".png",".jpeg"]]
image_paths = sorted(image_paths)[:120]  # limitar para demo

# Display grid
rows = (len(image_paths)+n_cols-1)//n_cols
idx = 0
for r in range(rows):
    cols = st.columns(n_cols)
    for c in cols:
        if idx >= len(image_paths):
            break
        p = image_paths[idx]
        pred, conf = predict_image(str(p))
        caption = f"{pred} ({conf:.2f})"
        if pred == "diseased":
            c.image(Image.open(p), caption=caption, use_column_width=True)
        else:
            c.image(Image.open(p), caption=caption, use_column_width=True)
        idx += 1

st.sidebar.markdown("### Nota")
st.sidebar.write("Modelo rápido para demonstração (embeddings + logistic regression).")
