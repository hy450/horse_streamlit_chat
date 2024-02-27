import streamlit as st
import time
import requests
import json
from audio_recorder_streamlit import audio_recorder

# Streamed response emulator
def response_generator(responseDatsa):    
    for word in responseDatsa.split():
        yield word + " "
        time.sleep(0.05)

st.title("KRA 챗봇")

with st.sidebar:
    
    model_radio = st.sidebar.radio("Select model",(
        "KoAlpaca","FineTuned"))
    st.sidebar.text("ver 022715")
    st.empty()

    if audio_bytes := audio_recorder(text="녹음",icon_size="3x"):
        st.audio(audio_bytes,format="audio/wav")    



print(model_radio)
    

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])    



# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})    


    data={
        'content': prompt
    }
    print(data)
    # REST API 를 호출해야함.    
    url = "http://3.39.53.42:8000/chat" if model_radio == "FineTuned" else "http://3.37.154.147:8000/chat"

    serverRsp = requests.post(url, json=data, headers={"Content-Type": "application/json"},verify=False)
    #print(json.dumps(serverRsp))
    #serverRsp = requests.get(url)
    if serverRsp.status_code == 200:
        #print(serverRsp.json())
        data = serverRsp.json()
        response = data["content"]       

    else:
        response = "에러가 발생하였습니다."


    #response = f"Echo: {prompt}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):        
        st.write_stream(response_generator(response))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

