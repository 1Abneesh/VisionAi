# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 00:36:09 2023

@author: Abneesh Kumar
"""


import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit.components.v1 import html
import base64



st.set_page_config(
    page_title="Flower species recognition",
    page_icon="🌻🌹",
    layout='wide',

)
st.markdown("""
<style>
    body {
        background-color: #2b2b2b;
    }
</style>
""", unsafe_allow_html=True)
# company logo taken from https://stackoverflow.com/questions/73251012/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-streamlit-multi
# from PIL import Image
# import streamlit as st

# You can always call this function where ever you want


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


custom_style = """
<style>
body {
  border: 10px solid blue;
  padding: 20px;
}
</style>
"""

st.markdown(custom_style, unsafe_allow_html=True)
col1,  col2,col3 = st.columns([1.2,2,1])
with col2:
    st.title("Flower species recognition")


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_flower = "https://assets9.lottiefiles.com/packages/lf20_molzhsbm.json"
lottie_flower = load_lottieurl(lottie_url_flower)

# col1,  col2 = st.columns([10,5])
# with col1:
#     st.write("We are making various model with high accuracy to predict diseases easily and fast.Our app is free of cost which take various patient data as input and predict what disease patient is suffering from.our model is trained on verified lab dataset and have high accuracy.Currently Diabetes prediction and stroke prediction is fully working is fully working and many others to come.Fell free to contact from contact form for any suggestion.🙂")
# with col2:
#     st_lottie(lottie_doctor, key="hello",speed=1, loop=True, quality="medium", width=300,height=200)
# st.write("")
# col1,col2,col3 = st.columns([1,2,1])
# with col2:
#     st.markdown("""**_"Eat fruits plenty, keep body wealthy."_**<br>""",True)

col1,col2,col3 = st.columns([1,2,1])
with col2:
    st_lottie(lottie_flower, key="hello",speed=1, loop=True, quality="medium", width=500,height=300)
# st.write('value and bring color and life to our surroundings, making great gifts for loved ones as well. Flowers play a crucial role in the ecosystem, providing food and shelter for pollinators and helping to maintain soil stability. They also have medical benefits, with some flowers being researched for their potential in treating serious medical conditions. Flowers are significant in the economy, with the global flower industry being worth billions of dollars, providing jobs and income for many communities. In addition, flowers have been a part of human culture for thousands of years, playing a role in religious and spiritual rituals and symbolizing different emotions. It is important to value and preserve flowers for their beauty, ecological benefits, medical benefits, economic benefits, and cultural significance.')

# import streamlit as st

header_html = "<h2 style='font-size:20pt;'>The Importance of Flowers</h2>"
st.markdown(header_html, unsafe_allow_html=True)

st.markdown("Flowers are one of the most important and beautiful aspects of nature. They have been cherished by humans for thousands of years and have played a significant role in our cultures and traditions. Flowers have numerous benefits that not only bring joy and beauty to our lives, but also provide numerous ecological and scientific benefits to the environment. In this article, we'll discuss the importance of flowers and why they should be valued and preserved for future generations.")

header_html1 = "<h2 style='font-size:15pt;'>Aesthetic value:</h2>"

st.markdown(header_html1, unsafe_allow_html=True)
st.markdown("Flowers are known for their stunning beauty, which adds color and life to our surroundings. Whether in gardens, parks, or as cut flowers in homes and public spaces, flowers provide a visual feast for the eyes and a sense of peace and calm. They also make great gifts for loved ones, providing an emotional and personal connection.")

header_html2 = "<h2 style='font-size:15pt;'>Ecological benefits:</h2>"

st.markdown(header_html2, unsafe_allow_html=True)
st.markdown("Flowers play an important role in the ecosystem. They provide food and shelter for pollinators like bees, butterflies, and birds, which are vital for maintaining a healthy environment. Flowers also help to maintain soil stability and prevent erosion by retaining moisture in the soil.")

header_html3 = "<h2 style='font-size:15pt;'>Medical benefits:</h2>"

st.markdown(header_html3, unsafe_allow_html=True)
st.markdown("Many flowers contain properties that have been used in traditional medicine for centuries. For example, chamomile flowers are known for their calming effect, while roses have been used to soothe skin irritations and reduce inflammation. Some flowers are even being researched for their potential in treating serious medical conditions such as cancer.")

header_html4 = "<h2 style='font-size:15pt;'>Economic benefits:</h2>"

st.markdown(header_html4, unsafe_allow_html=True)
st.markdown("Flowers play a significant role in the economy, with the global flower industry being worth billions of dollars. Flowers are grown and traded internationally, providing jobs and income for many communities, especially in developing countries.")

header_html5 = "<h2 style='font-size:15pt;'>Cultural significance:</h2>"

st.markdown(header_html5, unsafe_allow_html=True)
st.markdown("Cultural significance: Flowers have been an integral part of human culture for thousands of years. They play a significant role in religious and spiritual rituals, and are often used in festivals and celebrations, such as weddings and birthdays. Flowers also symbolize different emotions and are given as gifts to express love, gratitude, and sympathy.")


st.markdown("In conclusion, flowers play a vital role in our lives, providing beauty, ecological benefits, medical benefits, economic benefits, and cultural significance. They should be valued and preserved, not only for their beauty but also for their numerous contributions to our well-being and the health of the planet.")

st.write('Click on button below to know more about the working of app')



 
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#defining styling of button
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
    nav_page("info")

st.balloons()
# local_css("pages.css")
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("pages.css")