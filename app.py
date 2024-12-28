# app.py
import streamlit as st
from dotenv import load_dotenv
from components import create_chat_interface, create_sidebar
from models import ConversationManager

def init_session_state():
    """Initialize session state variables"""
    if "conversations" not in st.session_state:
        st.session_state.conversations = ConversationManager()

def main():
    # Load environment variables
    load_dotenv()
    
    # Page config
    st.set_page_config(
        page_title="Multi-Model Chat",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Create sidebar (includes model selection and conversation management)
    create_sidebar()
    
    # Create main chat interface
    create_chat_interface()

if __name__ == "__main__":
    main()
