# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:09:22 2023

@author: 01abn
"""

import requests
import streamlit as st
from streamlit_lottie import st_lottie
import base64
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Flower species recognition",
    page_icon="🌻🌹",
    layout='wide'
)

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

add_logo("logo.png")

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

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lootie_url = "https://assets10.lottiefiles.com/private_files/lf30_cmd8kh2q.json"
lottie_flower = load_lottieurl(lootie_url)

headers = """# How to use VisionAI"""
st.markdown(headers,unsafe_allow_html=True)

col1,col2,col3 = st.columns([1,2,1])
with col2:
    st_lottie(lottie_flower, key="hello",speed=1, loop=True, quality="medium", width=500,height=400)
    
content = """

1. Launch the app: 
    To launch the app, run the script that contains your Streamlit code. This will start a local web server and open the app in a browser.

2. Select an image: 
    In the app, you should have a button or file uploader that allows the user to select an image of a flower. Click the button or select an image from your device to upload it to the app.

3. Select a pretrained CNN model: 
    Before making a prediction, you can select from a list of pretrained CNN models. Choose the model that you want to use to make the prediction.

4. Wait for the prediction: 
    After the image and model are selected, the app will perform the necessary computations and make a prediction about the species of the flower in the image. This may take a few seconds, depending on the complexity of the model and the size of the image.

5. View the prediction: 
    The app will display the prediction results, including the top prediction for the species of the flower and its probability.

6. Repeat the process: 
    If you want to classify another flower species, you can repeat the steps 2-5 to get a prediction for a new image.

**Note:** The app's accuracy is greater than 75%, but there may still be some errors in the predictions. Always verify the predictions with additional sources before taking any action based on them.
"""
st.markdown(content,unsafe_allow_html=True)

header1 = """## Use case diagram of the App"""
st.markdown(header1,unsafe_allow_html=True)


st.image('use_case.png','Note: the app can classify more than 102 distinct species', width=600)

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
    nav_page("Flower")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("pages.css")