import streamlit as st
import time
import requests
import json

# Streamed response emulator
def response_generator(responseDatsa):    
    for word in responseDatsa.split():
        yield word + " "
        time.sleep(0.05)

st.title("KRA 챗봇")

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
    url = "https://ef59-3-39-53-42.ngrok-free.app/chat"
    serverRsp = requests.post(url, json=data, headers={"Content-Type": "application/json"})
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


