# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 03:13:41 2023

@author: 01abn
"""
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import base64
import webbrowser

st.set_page_config(
    page_title="DiagnosticAI",
    page_icon="👨‍⚕️",
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

add_logo("logo1.png")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url_download = "https://assets6.lottiefiles.com/packages/lf20_bkmppjns.json"
lottie_download = load_lottieurl(lottie_url_download)
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

def open_search(search_term):
    webbrowser.open(f"{search_term}")
col1,  col2,col3 = st.columns([1.2,2,1])
with col2:
    st.write("# DiagnosticAI")
    st_lottie(lottie_download, key="hello",speed=1, loop=True, quality="medium", width=700,height=500)



st.write("## Overview")
st.write("DiagnosticAI is a state-of-the-art machine learning app that is revolutionizing the field of healthcare.")
st.write("It utilizes advanced machine learning algorithms to diagnose various diseases such as diabetes and stroke, providing quick and accurate results with an accuracy rate of over 85%.")
st.write("This app is the epitome of cutting-edge technology, and is set to change the way healthcare is delivered.")

st.write("## Advanced Algorithms")
st.write("The app uses a combination of SVC (Support Vector Classifier) and Logistic Regression algorithms to analyze the symptoms of the patient and classify the disease accurately.")
st.write("The algorithms are trained on vast amounts of medical data, allowing the app to make highly informed diagnoses.")
st.write("This eliminates the need for multiple tests and procedures, saving time and money for both patients and healthcare professionals.")

st.write("## User-Friendly Interface")
st.write("The user-friendly interface of DiagnosticAI makes it easy for healthcare professionals to use the app, even if they have limited technical knowledge.")
st.write("The app requires the input of a patient's symptoms and then provides a diagnosis in a matter of minutes.")
st.write("This speed and accuracy are crucial in the early stages of disease diagnosis, allowing for prompt and effective treatment.")

st.write("## Benefits for Patients and Healthcare Professionals")
st.write("DiagnosticAI is not only beneficial for healthcare professionals, but also for patients.")
st.write("With this app, patients can receive a quick and accurate diagnosis without having to wait for days or weeks to receive results.")
st.write("This helps to eliminate the stress and anxiety that come with waiting for medical test results.")
st.write("Moreover, the app provides a clear and concise diagnosis, allowing patients to take control of their health and make informed decisions about their treatment.")

st.write("## Conclusion")
st.write("In conclusion, DiagnosticAI is a game-changer in the field of healthcare.")
st.write("With its advanced machine learning algorithms, accurate diagnoses, and user-friendly interface, it is set to revolutionize the way healthcare is delivered.")
st.write("Whether you are a healthcare professional or a patient, DiagnosticAI is a must-have app for anyone looking to stay ahead of the curve in this rapidly evolving field.")

col1,  col2,col3 = st.columns([1.2,2,1])
with col2:
    st.image('logo1.png',width=700)

st.write('')
st.write('')
st.header("Contact Us")
st.write("For any inquiries or questions, please contact us at 01abneeshkumar@gmail.com.")

st.write("")

search_link = f"https://multiple-disease-prediction-app.onrender.com/"

if st.button('DiagnosticAI'):
    open_search('https://multiple-disease-prediction-app.onrender.com/')

st.write('click on the link if button does not work')
st.markdown(f"[Search]({search_link})", unsafe_allow_html=True)
#applying css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("pages.css")