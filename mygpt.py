import streamlit as st
from openai import OpenAI
import json
import os
import pandas as pd
from PIL import Image

DB_FILE = 'db.json'
st.markdown("""
    <style>
    .title {
        font-size: 48px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    <div class="title">MyGPT : o1-mini</div>
    """, unsafe_allow_html=True)

def main():
    client = OpenAI(api_key=st.session_state.openai_api_key)

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "o1-mini"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

if 'openai_api_key' in st.session_state and st.session_state.openai_api_key:
    main()
else:
    print("ELSE Running")
    # if the DB_FILE not exists, create it
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as file:
            db = {
                'openai_api_keys': [],
                'chat_history': []
            }
            json.dump(db, file)
    # load the database
    else:
        with open(DB_FILE, 'r') as file:
            db = json.load(file)

    st.success("Key load successfully.")
    st.session_state['openai_api_key'] = db['openai_api_keys']
    st.rerun()