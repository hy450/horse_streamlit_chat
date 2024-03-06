import streamlit as st
import time
import requests
import json
from audio_recorder_streamlit import audio_recorder
from requests_toolbelt.multipart.encoder import MultipartEncoder


# Streamed response emulator
def response_generator(responseDatsa):    
    for word in responseDatsa.split():
        yield word + " "
        time.sleep(0.05)

def queryToChatbot(prompt):
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

    with st.chat_message("assistant"):
        st.write_stream(response_generator(response))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})        


st.title("KRA 챗봇")

with st.sidebar:
    model_radio = st.sidebar.radio("Select model",(
        "KoAlpaca","FineTuned"))
    st.sidebar.text("ver 030610")    

    if audio_bytes := audio_recorder(text="녹음",icon_size="3x"):
        st.audio(audio_bytes,format="audio/wav")
        with open("ko_read_ko1.wav",mode="wb") as f:
            f.write(audio_bytes)
            f.close()
            mp_encoder = MultipartEncoder(                
                fields={                                        
                    'audio_file': ( 'ko_read_ko1.wav', open("ko_read_ko1.wav", "rb"), 'audio/wav')                    
                }
            )                                    
            audioRsp = requests.post('http://15.164.1.44:9000/asr',data=mp_encoder, headers={'Content-Type': mp_encoder.content_type})
            rspJson = audioRsp.json()
            # print(rspJson['text'])
            st.session_state.messages.append({"role": "user", "content": rspJson['text']})    
            # queryToChatbot(prompt=rspJson['text'])          
            


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

    queryToChatbot(prompt=prompt)
    

