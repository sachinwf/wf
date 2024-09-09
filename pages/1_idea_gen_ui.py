import os
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain
from langchain_openai import ChatOpenAI

import hmac
import streamlit as st

st.title("Idea Generator and Validator (v1)")


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

if "model" not in st.session_state:
    st.session_state.model = "gpt-4"

def get_download_stream():
    download_text = ""
    for message in st.session_state.chat_history:
        download_text += f"{message['role']}: {message['content']}\n\n"
    return download_text


with st.sidebar:
    st.write("This chatbot helps you generate, refine and validates your ideas. Say \"Hello\" to start the interaction")
    option = st.selectbox("Select Model to use:", ("GPT 4", "GPT 4o", "GPT 3.5"))
    mapping_dict = {
        "GPT 4o": "gpt-4o",
        "GPT 4": "gpt-4",
        "GPT 3.5": "gpt-3.5-turbo",
    }
    st.success(f"Model selected: {option}")
    if "chat_history" not in st.session_state or st.session_state.model!=mapping_dict[option]:
        st.session_state.model=mapping_dict[option]
        st.session_state.chat_history = [{'role':'assistant', 'content':f"Model selected is {st.session_state.model}"}]
    
    st.download_button("Download chat", data=get_download_stream())


DEBUG=False
MODEL = st.session_state.model


if "memory" not in st.session_state:
    memory = ConversationBufferMemory()
else:
    memory = st.session_state.memory

system_message = st.secrets['system_message']
system_message+="""
The current conversation history is: {history}

User input is : {input}
"""
llm = ChatOpenAI(model=MODEL, api_key=st.secrets["openai_api_key"])

template = ChatPromptTemplate.from_template(system_message)

parser = StrOutputParser()

chain = ConversationChain(llm=llm,
    memory=memory,
    verbose=DEBUG,
    prompt=template,
)

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter your idea here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.chat_history.append({'role':'user', 'content':prompt})
    
    with st.chat_message("assistant"):
        response = chain.predict(input=prompt, history=memory.chat_memory)
        st.session_state.chat_history.append({'role':'ai', 'content':response})
        st.markdown(response)
        
    st.session_state.memory = memory
