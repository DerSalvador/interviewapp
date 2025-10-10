# utils.py
from openai import OpenAI

client = OpenAI()
import streamlit as st

def get_openai_api_key():
    return st.secrets["OPENAI_API_KEY"]

def moderate_input(prompt):
    # response = openai.Moderation.create(input=prompt)
    #return response["results"][0]["flagged"]
    return False

def call_openai(prompt, user_response, temperature=0.7):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_response}
    ]
    response = client.chat.completions.create(model="gpt-5",
    messages=messages,
    temperature=1,
    max_completion_tokens=500)
    return response.choices[0].message.content.strip()

