from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_core.messages import HumanMessage
import streamlit as st

from components import executor


if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        human_message = HumanMessage(content=[
            { "type": "text", "text": "Can I recycle it? Also any additional information if available would be helpful" },
            { "type": "image_url", "image_url": { "url": prompt }}
        ])
        response = executor.invoke({"input": human_message}, {"callbacks": [st_callback]})
        st.write(response["output"])
