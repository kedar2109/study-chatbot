# 💬 Study Chatbot (Computer Engineering Assistant)

This project is an **AI-powered chatbot** built using **LangChain**, **LangGraph**, **Streamlit**, and **Google Gemini** models.  
It acts as a **study assistant** for **Computer Engineering students**, answering only course-related questions (e.g., Data Science, OS, AI, ML, DBMS, etc.).

---

## 🚀 Features

- 🧠 Uses **Google Gemini (via LangChain)** for intelligent answers  
- 🧩 Built using **LangGraph** for conversation flow management  
- 💾 **SQLite-based conversation storage** for persistent chat history  
- 💬 **Multi-threaded chat sessions** (each chat has a unique Thread ID)  
- 🧍‍♂️ Streamlit frontend for smooth user interaction  
- 🔒 Automatically filters out unrelated questions (non–Computer Engineering)  

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **Backend** | LangChain + LangGraph |
| **LLM** | Google Gemini 2.5 Flash |
| **Database** | SQLite |
| **Environment** | Python (>=3.10) |

---

## 📂 Project Structure

```
📁 study_chatbot/
│
├── chatbot_backend.py     # Backend logic (LLM, LangGraph, and DB)
├── chatbot_ui.py          # Streamlit UI with chat handling
├── chatbot.db             # Auto-created SQLite database
├── .env                   # Store your Google API Key here
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/kedar2109/study-chatbot
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root and add your **Google Gemini API key**:

```
GOOGLE_API_KEY=your_api_key_here
```

You can get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## ▶️ Run the App

Run the Streamlit interface:

```bash
streamlit run chatbot_ui.py
```

Then open the URL (usually http://localhost:8501) in your browser.

---

## 🧩 How It Works

1. Each new chat session is assigned a **unique Thread ID** using `uuid`.
2. The backend (in `chatbot_backend.py`) maintains a **LangGraph** workflow:
   - Adds a **system message** enforcing domain-specific responses.
   - Stores conversation states in SQLite for persistence.
3. The frontend (in `chatbot_ui.py`):
   - Displays chat history and session list in a **Streamlit sidebar**.
   - Handles **new chat creation**, **message display**, and **AI responses**.
   - Saves chat names automatically based on the user’s first message.


---


## 👨‍💻 Author

**Kedar Desai**  
📧 kedardesai9005@gmail.com  

---
