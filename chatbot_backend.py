from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, SystemMessage
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from dotenv import load_dotenv
load_dotenv()
CONFIG={'configurable':{'thread_id':'thread-1'}}
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

model= ChatGoogleGenerativeAI(model='gemini-2.5-flash')

connection= sqlite3.connect(database='chatbot.db', check_same_thread=False)


connection.execute("""
CREATE TABLE IF NOT EXISTS chat_threads (
    thread_id TEXT PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
connection.commit()

def save_thread_name(thread_id: str, name: str):
    """Insert or update a thread name, preserving creation order."""
    connection.execute(
        """
        INSERT INTO chat_threads (thread_id, name, created_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(thread_id) DO UPDATE SET name=excluded.name
        """,
        (thread_id, name)
    )
    connection.commit()

def get_threads():
    """Get all threads with names, ordered by creation time (oldest first)."""
    cursor = connection.execute(
        "SELECT thread_id, name FROM chat_threads ORDER BY created_at ASC"
    )
    return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

def retrive_all_threads():
    """Return all thread IDs known to LangGraph checkpoint (raw)."""
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)

checkpointer=SqliteSaver(conn=connection)

def chat_node(state:ChatState):
    messages=state['messages']
    system_message = SystemMessage(
        content=(
            "You are an expert in engineering teacher. "
            "You will only answer questions related to computer engineering (e.g., Data Science, operating System, AI, computer science). "
            "If the question is unrelated to topic, politely respond with: "
            "'I can only answer questions related to Computer Engineering.'"
            "Give answers in maximum 20 lines"
        )
    )

    # Ensure system message is always included
    final_messages = [system_message] + messages

    response=model.invoke(final_messages)

    return {'messages':[response]}

def retrive_all_threads():
    all_threads= set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)    

graph= StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node', END)

chatbot= graph.compile(checkpointer=checkpointer )
