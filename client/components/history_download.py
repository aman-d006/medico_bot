import streamlit as st


def render_history_download():
    """Download chat history as a text file"""
    if "messages" in st.session_state and st.session_state.messages:
        chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button(
            "📥 Download Chat History",
            chat_text,
            file_name="chat_history.txt",
            mime="text/plain",
            key="download_history"
        )