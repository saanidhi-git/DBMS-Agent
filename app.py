import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="DBMA | Database Management Agent",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("DBMA - Database Management Agent")
st.markdown("*Chat with your database using natural language*")

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "my_db" not in st.session_state:
    st.session_state.my_db = None
if "db_path" not in st.session_state:
    st.session_state.db_path = None
if "db_name" not in st.session_state:
    st.session_state.db_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()
if "config" not in st.session_state:
    st.session_state.config = {"configurable": {
        "thread_id": "streamlit_session"}}

# Sidebar for database setup
with st.sidebar:
    st.header("⚙️ Database Setup")

    db_option = st.radio(
        "Choose database option:",
        ["Create New Database", "Load Existing Database"]
    )

    if db_option == "Create New Database":
        db_name = st.text_input(
            "Database name (without .db)",
            placeholder="my_database"
        )

        if st.button("Create Database", use_container_width=True):
            if db_name:
                try:
                    db_path = os.path.join("databases", f"{db_name}.db")
                    os.makedirs("databases", exist_ok=True)
                    st.session_state.my_db = SQLDatabase.from_uri(
                        f"sqlite:///{db_path}")
                    st.session_state.db_path = db_path
                    st.session_state.db_name = db_name
                    st.success(f"✅ Database created: {db_name}.db")
                except Exception as e:
                    st.error(f"❌ Error creating database: {str(e)}")
            else:
                st.warning("Please enter a database name")

    else:  # Load existing database
        st.markdown("**Upload your .db file:**")
        uploaded_file = st.file_uploader(
            "Choose a SQLite database file",
            type=["db", "sqlite", "sqlite3"],
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                temp_db_path = os.path.join("temp", uploaded_file.name)
                os.makedirs("temp", exist_ok=True)

                with open(temp_db_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Load the database
                st.session_state.my_db = SQLDatabase.from_uri(
                    f"sqlite:///{temp_db_path}")
                st.session_state.db_path = temp_db_path
                st.session_state.db_name = os.path.splitext(
                    uploaded_file.name)[0]
                st.success(f"✅ Database loaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"❌ Error loading database: {str(e)}")

    # Initialize agent if database is loaded
    if st.session_state.my_db and st.session_state.agent is None:
        try:
            with st.spinner("Initializing agent..."):
                llm = ChatGroq(
                    model="qwen/qwen3-32b", temperature=0)

                toolkit = SQLDatabaseToolkit(
                    db=st.session_state.my_db, llm=llm)
                st.session_state.agent = create_agent(
                    llm,
                    toolkit.get_tools(),
                    system_prompt="""
    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    You have access to tools for interacting with the database.
    Only use the below tools. Only use the information returned by the below tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    DO make USE of DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    To start you should ALWAYS look at the tables in the database to see what you can query.
    Do NOT skip this step.
    Then you should query the schema of the most relevant tables.

    DO NOT ask questions to the user. 
    You have access to the database and can query it directly, so there is no need to ask the user for more information.
    """,
                    checkpointer=st.session_state.memory
                )
            st.success("✅ Agent initialized")
            st.session_state.messages = []  # Clear messages on new agent init
        except Exception as e:
            st.error(f"❌ Error initializing agent: {str(e)}")

    st.divider()

    # Database info and download
    if st.session_state.my_db:
        st.subheader("📊 Database Info")
        try:
            tables = st.session_state.my_db.get_usable_table_names()
            st.write(
                f"**Tables:** {', '.join(tables) if tables else 'No tables'}")
        except:
            st.write("**Tables:** Unable to retrieve")

        # Download button
        st.divider()
        st.subheader("📥 Export Database")
        if st.session_state.db_path and os.path.exists(st.session_state.db_path):
            try:
                with open(st.session_state.db_path, "rb") as f:
                    db_file_data = f.read()

                st.download_button(
                    label="⬇️ Download Database",
                    data=db_file_data,
                    file_name=f"{st.session_state.db_name}_updated.db",
                    mime="application/x-sqlite3",
                    use_container_width=True
                )
                st.caption("📝 All updates from the agent are included")
            except Exception as e:
                st.error(f"❌ Error preparing download: {str(e)}")

    # Clear conversation button
    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
if st.session_state.agent is None:
    st.info("👈 Set up a database in the sidebar to get started!")
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask your database a question..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    events = st.session_state.agent.stream(
                        {"messages": [("user", prompt)]},
                        stream_mode="values",
                        config=st.session_state.config
                    )

                    response_text = ""
                    for event in events:
                        if "messages" in event:
                            last_message = event["messages"][-1]
                            response_text = last_message.content

                    st.markdown(response_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_text})

                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg})
