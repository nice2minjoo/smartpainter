import streamlit as st
import openai
from PyKakao import Karlo
import requests
import json
import io
import base64
from PIL import Image

OPENAI_API_KEY = "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"
KAKAO_API_KEY = "aae47d1d4531de86c0547401b169f52c"

st.title("smart painter")

with st.form("form"):
    query = st.text_input("Input")
    size = st.selectbox("Size", ["1024x1024","512x512","256x256"])
    submit = st.form_submit_button("Submit")

# certification of openai API key
openai.api_key = OPENAI_API_KEY

# create Karlo api instance
karlo = Karlo(service_key = KAKAO_API_KEY)

# select model GPT 3.5 turbo
model = "gpt-3.5-turbo"

# generate image using Karlo
def t2i(text, batch_size=1):
    r = requests.post(
        'https://api.kakaobrain.com/v1/inference/karlo/t2i',
        json = {
            'prompt': {
                'text': text,
                'batch_size': batch_size
            }
        },
        headers = {
            'Authorization': f'KakaoAK {KAKAO_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    # convert response in json format
    response = json.loads(r.content)
    return response

# Base64 decoding and  convert
def stringToImage(base64_string, mode='RGBA'):
    imgdata = base64.b64decode(str(base64_string))
    img = Image.open(io.BytesIO(imgdata)).convert(mode)
    return img
  
# question
if submit and query:
    # message
    messages = [
        {
            "role": "system",
            "content": "Imagine the details appearance of the input. Response it shortly around 20 words."
        },
        {
            "role": "user",
            "content": query
        }
    ]

    # add user message
    #messages.append(
        #{
            #"role": "user",
            #"content": "Condense up to 4 outward description to focus on nouns and adjectives separated by ,"
        #}
    #)

    # call ChatGPT API
    with st.spinner("Waiting for ChatGPT..."):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )

    answer = response['choices'][0]['message']['content']
    #print(answer)

    st.write(answer)

    with st.spinner("Waiting for Karlo..."):
      response = t2i(answer, 1)
      result = stringToImage(response.get("images")[0].get("image"), mode='RGB')

    if size == "1024x1024":
        user_size = 1024
    elif size == "512x512":
        user_size = 512
    elif size == "256x256":
        user_size = 256
        
    st.image(result, width = user_size)
