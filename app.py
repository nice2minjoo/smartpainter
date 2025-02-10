import streamlit as st
import openai

openai.api_key = st.secrets["api_key"]

st.title("smart painter")

with st.form("form"):
    user_input = st.text_input("Input")
    user_size = st.selectbox("Size", ["1024x1024","512x512","256x256"])
    submit = st.form_submit_button("Submit")

if submit and user_input:
    gpt_prompt = [
        {
            "role": "system",
            "content": "Imagine the details appearance of the input. Response it shortly around 20 words."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
    
    with st.spinner("Waiting for ChatGPT..."):
        gpt_response = openai.completions.create(
            model = "gpt-3.5-turbo",
            messages = gpt_prompt
        )
    
    finish_reason = gpt_response["choices"][0]["finish_reason"]
    if finish_reason != "stop":
        st.write("no more token")
    
    else:
        prompt = gpt_response["choices"][0]["message"]["content"]
        st.write(prompt)
        
        with st.spinner("Waiting for DALL-E..."):
            dalle_response = openai.images.generate(
                prompt = prompt,
                size = user_size
            )
            
        st.image(dalle_response["data"][0]["url"])
    
elif not user_input and submit:
    st.write("please try again")
