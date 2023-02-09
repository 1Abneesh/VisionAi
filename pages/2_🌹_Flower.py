# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 16:45:22 2023

@author: 01abn
"""



#importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import torch
import PIL
import math
from torch import nn
import argparse
import json
from torch import optim
from torchvision import datasets, models, transforms
from collections import OrderedDict
from torchvision import models
from PIL import Image
import torch.nn.functional as F
import torch.utils.data
import pandas as pd
import streamlit as st
import base64
import requests
from streamlit_lottie import st_lottie
import webbrowser
from streamlit_lottie import st_lottie_spinner
import time
from streamlit.components.v1 import html
# define Mandatory and Optional Arguments for the script
# def arg_parser():
#     parser = argparse.ArgumentParser(description="predict.py")
    
#     parser.add_argument('--image',type=str,help='Point to image file for prediction.',required=True)
#     parser.add_argument('--category_names', dest="category_names", action="store", default='cat_to_name.json')
#     parser.add_argument('--checkpoint',type=str,help='Point to checkpoint file as str.',required=True)
#     parser.add_argument('--gpu', default="gpu", action="store", dest="gpu")
#     parser.add_argument('--top_k',type=int,help='Choose top K matches as int.')

#     args = parser.parse_args()
#     return args


st.set_page_config(page_title="Image Input", page_icon=":camera:", layout="wide")

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ce1126;
    color: white;
    height: 3em;
    width: 12em;
    border-radius:10px;
    border:3px solid #000000;
    font-size:20px;
    font-weight: bold;
    margin: auto;
    display: block;
}

div.stButton > button:hover {
	background:linear-gradient(to bottom, #ce1126 5%, #ff5a5a 100%);
	background-color:#ce1126;
}

div.stButton > button:active {
	position:relative;
	top:3px;
}

</style>""", unsafe_allow_html=True)

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
def build_markup_for_logo(
    png_file,
    background_position="50% 10%",
    margin_top="10%",
    image_width="60%",
    image_height="",
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
    )


def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )


torch.nn.Module.dump_patches = True



def open_search(search_term):
    webbrowser.open(f"https://www.google.com/search?q={search_term}")


#checking for GPU avilability
def check_gpu(gpu_arg):
    if not gpu_arg:
        return torch.device("cpu")   
    elif gpu_arg == "cpu":
        return torch.device("cpu")
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    return device

def predict(image_path, model,device, topk=5):
    ''' Predict the class (or classes) of an image using a trained deep learning model.
    '''
    lottie_url_download = "https://assets2.lottiefiles.com/packages/lf20_kvw2mn6a.json"
    lottie_download = load_lottieurl(lottie_url_download)
    with st_lottie_spinner(lottie_download, key="download",height=100,width=200):
        time.sleep(5)
    model.to(device)
    model.eval();
    print('Device ' ,device)
    # Convert image from numpy to torch
    torch_image = torch.from_numpy(np.expand_dims(image_path, axis=0)).type(torch.FloatTensor).to(device)

    # Find probabilities (results) by passing through the function (note the log softmax means that its on a log scale)
    log_probs = model.forward(torch_image)

    # Convert to linear scale
    linear_probs = torch.exp(log_probs)

    # Find the top 5 results
    top_probs, top_labels = linear_probs.topk(topk)
    top_probs = np.array(top_probs.detach())[0] 
    top_labels = np.array(top_labels.detach())[0]
    with open('cat_to_name.json', 'r') as f:
        cat_to_name = json.load(f)
    # Convert to classes
    idx_to_class = {val: key for key, val in model.class_to_idx.items()}
    top_labels = [idx_to_class[lab] for lab in top_labels]
    top_flowers = [cat_to_name[lab] for lab in top_labels]
    
    return top_probs, top_labels, top_flowers


# Scales, crops, and normalizes a PIL image for a PyTorch model,returns an Numpy array
def process_image(image):
    ''' Scales, crops, and normalizes a PIL image for a PyTorch model,
        returns an Numpy array
    '''
    
    # TODO: Process a PIL image for use in a PyTorch model
        #size = 256, 256
    #loading image
    # im = PIL.Image.open (image) 
    #original size
    im = image
    width, height = im.size

    if width > height: 
        height = 256
        
    else: 
        width = 256
    im.thumbnail ((width,50000), Image.ANTIALIAS) 
    #new size of im
    width, height = im.size 
    #crop 224x224 in the center
    reduce = 224
    left = (width - reduce)/2 
    top = (height - reduce)/2
    right = left + 224 
    bottom = top + 224
    im = im.crop ((left, top, right, bottom))
    
    #preparing numpy array
    #to make values from 0 to 1
    numpy_img = np.array(im)/255 
    # Normalize each color channel
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    numpy_img = (numpy_img-mean)/std
    
    numpy_img= numpy_img.transpose ((2,0,1))
    return numpy_img



def print_probability(probs, flowers):
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"<h1><span style='color:#FCF9F9'>The given flower is:</span></h1>", unsafe_allow_html=True)
    prob = probs[0]
    col1,col2,col3 = st.columns([1.1,2,1])
    with col2:
        st.markdown(f"<h2><span style='color:#F8F8FF'>{prob}</span></h2>", unsafe_allow_html=True)
    for i, j in enumerate(zip(flowers, probs)):
        st.write("(liklihood: {}%)".format(math.ceil(j[0]*100)))

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# def upload_image():
def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)    


def not_flower(image):

    lootie_url = "https://assets1.lottiefiles.com/temp/lf20_QYm9j9.json"
    lottie_flower = load_lottieurl(lootie_url)

    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st_lottie(lottie_flower, key="hello",speed=1, loop=True, quality="medium", width=500,height=400)
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st.image(image, caption='Uploaded Image.', width=300)
        st.markdown("<h2><span style='color:red'>The given image is of not flower</span></h2>", unsafe_allow_html=True)
# Loading the trained model
def load_checkpoint(checkpoint_path):
    checkpoint = torch.load(checkpoint_path) 
    model = models.vgg19(pretrained=True)
    model.name = "vgg19"
    for param in model.parameters(): 
        param.requires_grad = False
#     print(checkpoint.keys)
    # Load from checkpoint
    model.classifier = checkpoint['classifier']
    model.load_state_dict(checkpoint['state_dict'])
    model.class_to_idx = checkpoint['mapping']
    return model
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
#taking all the arguments
def main():
    # args = arg_parser()
    add_logo("logo.png")
    st.header('FLower species prediction using pretrained vgg19 Network')
    
    lootie_url = 'https://assets9.lottiefiles.com/packages/lf20_l0segmbm.json'
    lootie_robot = load_lottieurl(lootie_url)

    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st_lottie(lootie_robot, key="hello2",speed=1, loop=True, quality="medium", width=500,height=400)
    
    category_names = 'cat_to_name.json'
    with open(category_names, 'r') as f:
        cat_to_name = json.load(f)
        #load the trained models
    model = load_checkpoint('checkpoint.pth')
    
    
    option = st.selectbox("Please select an option for uploading an image:", ["Take a photo", "Upload an image"])

# Take a photo or upload an image based on the user's selection
    if option == "Take a photo":
        # Code for accessing the camera and capturing an image
        camera_input = st.camera_input("Take a picture:")
        # image = Image.open(camera_input)
        # Display the captured image
        if camera_input:
            st.write("Image uploaded")
            image = Image.open(camera_input)
            
            
            image_tensor = process_image(image)
            #checkng for available device
            device = check_gpu('gpu');
            #getting the predictions
            top_probs, top_labels, top_flowers = predict(image_tensor,model,device,1)
            # print(top_probs)
            if top_probs[0]<0.12:
                print(top_probs)
                not_flower(image)
            else:
                col1,col2,col3 = st.columns([1,2,1])
                with col2:
                    st.image(image, caption='Uploaded Image.', width=500)
                print_probability(top_flowers, top_probs)
                search_term = top_flowers            
                if search_term:
                    if st.button("Google Search"):
                        open_search(search_term)
    elif option == "Upload an image":
        # Code for uploading an image file
        uploaded_file = st.file_uploader("Choose an image for prediction greater than 400KB...", type=["jpg", "jpeg", "png", "gif"])   
        
        
        if uploaded_file:
            st.write("Image uploaded")
            image = Image.open(uploaded_file)
            
            
            image_tensor = process_image(image)
            #checkng for available device
            device = check_gpu('gpu');
            #getting the predictions
            top_probs, top_labels, top_flowers = predict(image_tensor,model,device,1)
            # print(top_probs)
            if top_probs[0]<0.15:
                not_flower(image)
            else:
                col1,col2,col3 = st.columns([1,2,1])
                with col2:
                    st.image(image, caption='Uploaded Image.', width=500)
                print_probability(top_flowers, top_probs)
                search_term = top_flowers 
                if search_term:
                    if st.button("Google Search"):
                        open_search(search_term[0])


    local_css("pages.css")
if __name__ == "__main__":
    main()

    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #ce1126;
        color: white;
        height: 3em;
        width: 12em;
        border-radius:10px;
        border:3px solid #000000;
        font-size:20px;
        font-weight: bold;
        margin: auto;
        display: block;
    }

    div.stButton > button:hover {
    	background:linear-gradient(to bottom, #ce1126 5%, #ff5a5a 100%);
    	background-color:#ce1126;
    }

    div.stButton > button:active {
    	position:relative;
    	top:3px;
    }

    </style>""", unsafe_allow_html=True)

    if st.button("Next page"):
        nav_page("Contact_me")