import streamlit as st
from  backend import chatbot

with st.chat_message("user"):
    st.text("hi")

with st.chat_message("assistant"):
    st.text("how can you help me")


user_input  = st.chat_input("Type your message here")
if user_input:
    with st.chat_message("user"):
        st.text(user_input)
        