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


model_radio = st.sidebar.radio("Select model",(
    "KoAlpaca","FineTuned")
)
st.sidebar.text("ver 022715")

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

    serverRsp = requests.post(url, json=data, headers={"Content-Type": "application/json",'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'},verify=False)
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


