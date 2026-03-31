from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

memory = MemorySaver()

llm = ChatOllama(model="deepseek-v3.1:671b-cloud", temperature=0)

# asking user whether to create a new database or use an existing one
create_new_db = input(
    "\nDo you want to create a new database? (yes/no): ").strip().lower()

# if yes then ask for the name of the new database and create it, otherwise ask the user to upload his existing database file and use it
if create_new_db == "yes":
    ask_db_name = input(
        "\nEnter the name of the new database (without .db extension): ").strip()
    my_db = SQLDatabase.from_uri(f"sqlite:///{ask_db_name}.db")
    print(f"✅Successfully created new database: {ask_db_name}.db")

elif create_new_db == "no":
    db_file_path = input(
        "\nEnter the path to your existing database file (including .db extension): ").strip()
    my_db = SQLDatabase.from_uri(f"sqlite:///{db_file_path}")
    print(f"✅Successfully loaded the existing database from: {db_file_path}")

else:
    print("Invalid input. Please enter 'yes' or 'no'.")
    exit()


toolkit = SQLDatabaseToolkit(db=my_db, llm=llm)

print("\nHere are the tables in your database:")
print(my_db.get_usable_table_names())

agent = create_agent(
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

    DO NOT ask questions to the user. Ask for clarification only if absolutely necessary.
    You have access to the database and can query it directly, so there is no need to ask the user for more information.
    """,
    checkpointer=memory
)

config = {"configurable": {"thread_id": "12345"}}

while True:
    example_query = input("\nEnter query: ")
    if example_query.lower() == "exit":
        break

    events = agent.stream(
        {"messages": [("user", example_query)]},
        stream_mode="values",
        config=config
    )
    for event in events:
        event["messages"][-1].pretty_print()
