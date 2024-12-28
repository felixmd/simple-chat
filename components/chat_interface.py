# components/chat_interface.py
import streamlit as st
from models import Message, Role
from typing import Optional

def format_message_content(content: str) -> str:
    """Format message content with special handling for code blocks"""
    if "```" not in content:
        return content

    formatted_parts = []
    is_code_block = False
    
    for part in content.split("```"):
        if is_code_block:
            code_lines = part.split('\n')
            lang = code_lines[0].strip() or "python"
            code = '\n'.join(code_lines[1:] if lang != code_lines[0] else code_lines)
            formatted_parts.append(f"```{lang}\n{code}\n```")
        else:
            formatted_parts.append(part)
        is_code_block = not is_code_block
    
    return ''.join(formatted_parts)

def display_message(role: str, content: str):
    """Display a single message in the chat interface"""
    with st.chat_message(role):
        st.markdown(format_message_content(content), unsafe_allow_html=True)

def create_chat_interface():
    """Create the main chat interface"""
    st.title("Chat Interface")
    
    conversation = st.session_state.conversations.get_active_conversation()
    if not conversation:
        st.info("Create a new chat to begin!")
        return
    
    # Display current model
    st.caption(f"Current Model: {conversation.selected_model}")
    
    # Display existing messages
    for message in conversation.messages:
        display_message(message.role.value, message.content)
    
    # Chat input and response handling
    if prompt := st.chat_input("Type your message here..."):
        # Display user message
        display_message("user", prompt)
        user_message = Message(content=prompt, role=Role.USER)
        conversation.add_message(user_message)
        
        # Handle assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                for response_chunk in conversation.api_client.generate_stream_response(
                    messages=conversation.messages,
                    model=conversation.selected_model
                ):
                    full_response += response_chunk
                    message_placeholder.markdown(
                        format_message_content(full_response + "▌")
                    )
                
                # Final formatted message
                message_placeholder.markdown(format_message_content(full_response))
                assistant_message = Message(content=full_response, role=Role.ASSISTANT)
                conversation.add_message(assistant_message)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

