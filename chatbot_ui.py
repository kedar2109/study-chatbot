import streamlit as st
from chatbot_backend import chatbot, save_thread_name, get_threads

from langchain_core.messages import HumanMessage
import uuid

# Utility functions
def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id 
    add_thread(thread_id, name="New Chat")
    save_thread_name(thread_id, "New Chat")   # persist in DB
    st.session_state['message_history'] = []

def add_thread(thread_id, name="New Chat"):
    if not any(t["id"] == thread_id for t in st.session_state['chat_threads']):
        st.session_state['chat_threads'].append({"id": thread_id, "name": name})

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable':{'thread_id':thread_id}})
    return state.values.get('messages', [])   # safe lookup


# ---------------- INIT SESSION STATE ----------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    # Load threads directly from DB with correct order
    st.session_state['chat_threads'] = get_threads()

add_thread(st.session_state['thread_id'])


# ---------------- SIDEBAR ----------------
st.sidebar.title("Chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My conversations")

for thread in reversed(st.session_state['chat_threads']):
    if st.sidebar.button(thread["name"], key=thread["id"]):
        st.session_state['thread_id'] = thread["id"]
        messages = load_conversation(thread["id"])

        temp_msg = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_msg.append({'role': role, 'content': msg.content})
        st.session_state['message_history'] = temp_msg


# ---------------- MAIN CHAT UI ----------------

st.markdown("<h1 style='text-align: center;'>Study Chatbot🎓</h1>", unsafe_allow_html=True)
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

CONFIG = {'configurable':{'thread_id':st.session_state['thread_id']}}

if user_input:
    # Add user message to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # --- Auto name conversation on first user input ---
    current_thread = next(
        (t for t in st.session_state['chat_threads'] if t["id"] == st.session_state['thread_id']),
        None
    )
    if current_thread and current_thread["name"] == "New Chat":
        preview = " ".join(user_input.split()[:6])  # first 6 words
        new_name = preview if preview else "Conversation"
        current_thread["name"] = new_name
        save_thread_name(current_thread["id"], new_name)   # persist in DB

    # AI response
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
