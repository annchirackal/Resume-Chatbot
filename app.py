
import streamlit as st
from streamlit_chat import message
from resume_chat import resume_chatbot
from Logs.chat_logger import log_message  

class AnnChatApp:
    def __init__(self):
        # Initialize chatbot
        self.chatbot = resume_chatbot()

        # Set up the Streamlit page
        st.set_page_config(page_title="Ann's Interactive Chat", layout="centered")
        self._setup_ui()
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        
    def _setup_ui(self):
        st.title("🗣️ Ann's AI Assistant")
        st.markdown("""
        Hi! I’m Ann’s AI Assistant. You can ask me anything about Ann Maria Chirackal George’s experience, skill set, projects, or qualifications.
        \nI’m here to help you quickly understand how she can contribute to your team — especially for roles in Data Science, Applied Science, or Generative AI.
        \nYou can reach out to Ann at annchirackal@gmail.com.
        """)

    def _clear_input(self):
        st.session_state["user_input"] = ""

    def run(self):
        # Get user input
        user_input = st.text_input("Your message:", key="user_input")

        # Process the message
        if user_input:
            # Store user message
            st.session_state["messages"].append({"role": "user", "content": user_input})
            log_message("User", user_input)  # Log user message
            
            # Get chatbot response
            response = self.chatbot.get_answer(user_input)
            st.session_state["messages"].append({"role": "assistant", "content": response})
            log_message("Assistant", response)  # Log bot response

        # Display chat history
        for msg in st.session_state["messages"]:
            message(msg["content"], is_user=(msg["role"] == "user"))


# Run the chatbot
if __name__ == "__main__":
    app = AnnChatApp()
    app.run()
