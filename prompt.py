import streamlit as st
import numpy as np
# import os
from openai import OpenAI
# os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = os.environ['OPENAI_API_KEY']
api_key = st.secrets["OPENAI_API_KEY"]
# client = OpenAI(
#     organization='org-0JKgTOfmp6XDLqNF8XhBS4y8',
#     project='proj_Wf5Wl3EDZaYXlercWbXzliNJ'
# )

client = OpenAI(api_key=api_key)
prompt_instructions = "Generate a one-liner joke to defuse a rumor based on fact-check reports, considering the specified type of joke by the user.\n\n# Steps\n\n1. **Analyze the Rumor:** Understand the contents and context of the rumor that needs defusing.\n2. **Review Fact-Check Report:** Summarize the key points or findings that contradict the rumor.\n3. **Select Joke Type:** Identify the type of joke the user specifies.\n4. **Create the Joke:** Use the understanding of the rumor, the fact-check insights, and the specified joke type to craft a humorous one-liner that effectively debunks the rumor.\n\n# Output Format\n\nProvide a single sentence that is a one-liner joke, appropriate in style and substance to the context and the user’s preference for humor type. Output a meme if an image is provided.\n\n# Types of Jokes:\n\n1. **Dry/Factual:** Humor delivered with little emotion, relying on understatement and contrast between tone and content.\n2. **Sarcastic:** Irony used to mock or convey contempt, often with a biting or sharp tone.\n3. **Witty:** Clever, sharp use of language, including puns, double meanings, and retorts. This form of humor showcases intellectual dexterity.\n\n# Examples\n\n**Example 1:**\n- **Rumor:** \"Aliens built the pyramids.\"\n- **Fact:** Archaeologists have evidence of ancient Egyptian workers.\n- **Joke Type:** Dry/Factual\n- **Joke:** \"Oh yes, because nothing says extraterrestrial technology like hauling massive rocks with zero power tools.\"\n\n**Example 2:**\n- **Rumor:** \"Chocolate cures all diseases.\"\n- **Fact:** There is no scientific evidence supporting this.\n- **Joke Type:** Sarcastic\n- **Joke:** \"Of course, because why fund medical research when chocolate is clearly the miracle cure we've all missed?\"\n\n**Example 3:**\n- **Rumor:** \"The moon landing was faked.\"\n- **Fact:** Multiple sources confirm the authenticity of the Apollo missions.\n- **Joke Type:** Witty\n- **Joke:** \"Yes, because Hollywood in the '60s was advanced enough to outshine NASA? I'd like to see Kubrick pull that off.\"\n\n(Real jokes should closely adhere to the structure and humor specified in the user’s request with appropriate placeholders for factual input and humor type.)"

def generate_response(claim, fact, response_type, inputs):

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": prompt_instructions
                }
            ]
            },
            {
                "role":"user",
                "content": "Claim:" + claim + "\n# Fact:"+ fact + "\n# Additional instructions:" + inputs + "\n# Response type:" + response_type
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )
    
    final_response = response.choices[0].message.content
    
    return final_response

def generate_additional_response(claim, fact, response_type, history, inputs):

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": prompt_instructions
                }
            ]
            },
            {
                "role":"user",
                "content": "Claim:" + claim + "\n# Fact:"+ fact + "\n# Past history:" + history + "\n# New instructions:" + inputs + "\n# Response type:" + response_type
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )
    
    final_response = response.choices[0].message.content
    
    return final_response