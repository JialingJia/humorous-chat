import streamlit as st
import os

st.set_page_config(
    page_title='Humorous Response to Misinfo',
    page_icon='🤪',
    # layout='wide'
)

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.subheader("1️⃣ Initiate a fact-check in the message app", divider='blue')
st.image('images/Slide_1.png')

st.subheader("2️⃣ Select humorous response", divider='blue')
st.image('images/Slide_2.png')

st.subheader("3️⃣ Reply the message", divider='blue')
st.image('images/Slide_3.png')

st.subheader("4️⃣ Alternative condition: cannot find evidence", divider='blue')
st.image('images/Slide_4.png')