import streamlit as st
from assistant import Assistant

st.title("Ассистент по внутренней базе знаний Ultralitics")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        assistant = Assistant()
        response = assistant.ask(prompt).message.content
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})