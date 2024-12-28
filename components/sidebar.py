# components/sidebar.py
import streamlit as st
from typing import Dict
from utils.config import create_model_config

def create_sidebar():
    """Create the sidebar with model selection and conversation controls"""
    with st.sidebar:
        st.title("Settings")
        
        # Model selector
        model_config = create_model_config()
        selected_model = st.selectbox(
            "Select Model",
            list(model_config.keys()),
            help="Choose the AI model for this conversation"
        )
        
        # New chat button
        if st.button("New Chat", type="primary"):
            st.session_state.conversations.create_conversation(
                model_name=selected_model
            )
            st.rerun()
        
        # Display existing conversations
        st.divider()
        st.subheader("Your Conversations")
        
        for conv_id, model, msg_count in st.session_state.conversations.list_conversations():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                if st.button(f"Chat {msg_count} msgs", key=f"chat_{conv_id}"):
                    st.session_state.conversations.switch_conversation(conv_id)
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{conv_id}"):
                    st.session_state.conversations.delete_conversation(conv_id)
                    st.rerun()
