# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get responses

def get_gemini_response(input, image):
    if image:
        model_type = 'gemini-pro-vision'
    else:
        model_type = 'gemini-pro'
    model = genai.GenerativeModel(model_type)
    if input and image:
        response = model.generate_content([input, image])
    elif input:
        response = model.generate_content(input)
    elif image:
        response = model.generate_content(image)
        print(response)
    else:
        response = "Please provide input or upload an image."
        return response
    
    return response.text

## initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

header_text = "Assistance and Guidance on medical information for Lovely Vinni 😍 💖"
header_color = "pink"  # You can use any valid CSS color name or code

# Create a styled header using st.markdown
st.markdown(f'<h1 style="color: {header_color};">{header_text}</h1>', unsafe_allow_html=True)

# Use st.session_state to store and clear the input
def clear_text():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget=''

st.text_input('Enter text here:', key='widget', on_change=clear_text)
my_text = st.session_state.get('my_text', '')
# st.session_state.input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
else:
    image=None 

submit = st.button("Tell me about the inputs")

## If the ask button is clicked
# clear_inputs = st.checkbox("Clear Response")
# if clear_inputs:
#     st.session_state.my_text = ''
    
if submit:
    response = get_gemini_response(my_text, image)
    st.subheader("The Response is")
    st.write(response)
    st.session_state.my_text=''
    
    # Clear the input using st.session_state
    
