import streamlit as st
import numpy as np
import pandas as pd
import time
from prompt import generate_response, generate_additional_response

st.set_page_config(
    page_title='Humorous Response to Misinfo',
    page_icon='🤪',
    layout='wide'
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

if 'clicked' not in st.session_state:
    st.session_state.clicked = False
    st.session_state.response = ''
    
def click_button():
    st.session_state.clicked = True

def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("claims.csv")

response_style = {
    "Dry/Factual":"To the point, gives facts",
    "Sarcastic":"Irony used to mock or convey contempt, often with a biting or sharp tone",
    "Witty":"Clever, sharp use of language, including puns, double meanings, and retorts. This form of humor showcases intellectual dexterity."
}

col1, col2 = st.columns(2)

with col1:
    message = st.chat_message('assistant')
    message.write("Hi! I’m the correction bot! I’m here to support you in correcting misinformation. Specifically, I can take a misinformation claim and help provide some language to correct it. Please reply with the claim you want debunked.")
    claim_category = message.selectbox(
        "Choose a category from the following?",
        ("Politics", "Entertainment", "Health"),
        index=None,
        placeholder="Select claim topics...",
        )
    
    if claim_category:
        claim = message.radio(
            "Select a claim 👉",
            key="visibility",
            options=df[df['Type'] == claim_category]['Claim'])
        humor = message.selectbox(
            "Choose the style of response",
            ("Dry/Factual", "Sarcastic", "Witty"),
            index=None,
            placeholder="Select response style...",
            )
        if humor:
            message.write(response_style[humor])
            prompt = message.text_input('Add your own instructions (optional):')
    if claim_category and humor:
        submit = message.button("response")
        if submit:
            click_button()

with col2:
    check = st.chat_message('assistant')
    if claim_category:
        if st.session_state.clicked:
            check.write('Here is your fact-check response:')
            if submit:
                summary = df[(df['Type'] == claim_category) & (df['Claim'] == claim)]['Summary'].to_list()[0]
                source = df[(df['Type'] == claim_category) & (df['Claim'] == claim)]['Source'].to_list()[0]
                with st.status("thinking...") as status:
                    st.session_state.response = generate_response(claim, summary, humor, prompt)
                    time.sleep(1)
                    final_response = check.write(st.session_state.response)
                    check.write("Source: " + source)
                    status.update(label="Completed")
                # if prompt: 
                #     summary = df[(df['Type'] == claim_category) & (df['Claim'] == claim)]['Summary'].to_list()[0]
                #     source = df[(df['Type'] == claim_category) & (df['Claim'] == claim)]['Source'].to_list()[0]
                #     with st.status("thinking...") as status:
                #         st.session_state.response = generate_additional_response(claim, summary, humor, response, prompt)
                #         time.sleep(1)
                #         final_response = check.write(st.session_state.response)
                #         check.write("Source: " + source)
                #         status.update(label="Completed")
        else:
            check.write('Waiting for your selection...')
    else:
        check.write('I will provide a fact-check for your selected claims.')
        