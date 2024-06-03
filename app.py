from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_core.messages import HumanMessage
import streamlit as st

from components import (
    executor,
    upload_image,
)
# st.image("./image/logo.webp", width=400)
st.title("AI Recycling Assistant 🤖♻️")

if img_file_buffer := st.camera_input("Take a picture for the AI Assistant to help you with recycling"):
    url = upload_image(img_file_buffer)
    st.chat_message("user").write(url)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        human_message = HumanMessage(content=[
            { "type": "text", "text": "Can I recycle it? Also any additional information if available would be helpful" },
            { "type": "image_url", "image_url": { "url": url }}
        ])
        response = executor.invoke({"input": human_message}, {"callbacks": [st_callback]})
        st.write(response["output"])
