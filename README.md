# Database Management Agent (DBMA)

> Chat with your database using natural language powered by AI

## 🌟 Overview

**Database Management Agent** is an intelligent Streamlit-based application that allows users to interact with SQLite databases using natural language. Powered by Groq AI and LangChain, it converts your questions and commands into optimized SQL queries, eliminating the need to write SQL manually.

Whether you want to query data, insert records, update information, or analyze your database—just ask in plain English and let the AI handle the rest!

---

## ✨ Key Features featuring strong unique solutions

### 💬 Natural Language Interface

- Ask questions in plain English instead of writing SQL
- Get instant answers from your database
- No SQL knowledge required

### 🗂️ Flexible Database Management

- **Create new databases** instantly with a simple name
- **Upload existing `.db` files** directly from your laptop
- Support for `.db`, `.sqlite`, and `.sqlite3` formats

### 🔄 Full Database Operations

- **SELECT** - Query and retrieve data
- **INSERT** - Add new records
- **UPDATE** - Modify existing data
- **DELETE** - Remove records
- **ALTER** - Modify table structures
- **CREATE/DROP** - Table management

### 💾 Data Export

- Download updated databases with all changes
- Export your modified database back to your computer
- Preserve all AI-made modifications

---

## 📦 Installation

### 1. Clone or Download the Project

```bash
git clone https://github.com/yourusername/dbma.git
cd dbma
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Ollama (Required for AI)

- Download and install [Ollama](https://ollama.ai)
- Pull the DeepSeek model:

```bash
ollama pull deepseek-v3.1:671b-cloud
```

- Start Ollama server (usually runs on port 11434)

### 5. Configure Environment

Create a `.env` file (optional):

```env
# Add any configuration here if needed
```

---

## 🚀 Quick Start

### Run the Application

```bash
streamlit run app.py
```

The app opens at **<http://localhost:8501>**

### Basic Workflow

**Step 1: Set up Database**

- Choose "Create New Database" or "Load Existing Database"
- If creating: Enter a database name
- If loading: Upload your `.db` file

**Step 2: Ask Questions**

- Type your query in the chat box
- Examples:
  - "Show me all students"
  - "How many records do we have?"
  - "Add a new student named John"
  - "Update the age for user 5"
  - "Delete records older than 2020"

**Step 3: Download Results**

- After making changes, click "⬇️ Download Database"
- Your updated database is ready to use!

---

## 📝 Usage Examples

### Querying Data

```
User: "Show me the top 5 students with highest grades"
Agent: Creates SELECT query, retrieves and displays results
```

### Adding Data

```
User: "Add a new student named Alice, age 20, grade A"
Agent: Constructs INSERT query, adds record, confirms operation
```

### Updating Data

```
User: "Update John's grade to B+"
Agent: Finds John, updates grade, shows affected rows
```

### Analysis

```
User: "How many students are in each class?"
Agent: Creates GROUP BY query, displays summary
```

---

## 🏗️ Project Structure

```
dbma/
├── app.py                 # Main Streamlit application
├── main.py               # CLI version of the agent
├── main.ipynb            # Jupyter notebook for experimentation
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (optional)
├── README.md             # This file
├── databases/            # Created databases stored here
├── temp/                 # Uploaded databases stored here
└── .venv/                # Virtual environment
```

---

## ⚙️ Configuration

### Model Selection

To use a different AI model, edit line 94 in `app.py`:

```python
llm = ChatOllama(model="your-model-name", temperature=0)
```

Available Ollama models: [ollama.ai/library](https://ollama.ai/library)

### Result Limit

Change default result limit in system prompt (currently 5 rows)

### Session Thread ID

Modify in `app.py` for multi-user scenarios:

```python
st.session_state.config = {"configurable": {"thread_id": "unique_id"}}
```

---

## 🎯 Use Cases

✨ **Data Analysis** - Quickly query and analyze database content  
📊 **Data Management** - Insert, update, and manage records without SQL  
🔍 **Database Exploration** - Understand database structure and content  
📱 **Rapid Prototyping** - Quickly test database operations  
🎓 **Learning** - Great tool for beginners to learn databases  
🚀 **Business Intelligence** - Extract insights from data easily  

---


If you find DBMA useful, please star this repository! Your support motivates continued development.

**Made with ❤️ for database lovers everywhere**

---

## 🔗 Quick Links

- [Ollama Documentation](https://ollama.ai)
- [LangChain Docs](https://python.langchain.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [SQLite Reference](https://www.sqlite.org/docs.html)

---

*Last Updated: March 2026*
