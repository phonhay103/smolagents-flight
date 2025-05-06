import os
import streamlit as st
from smolagents import CodeAgent, LiteLLMModel, ToolCallingAgent
from tools.serpapi_tools import GoogleFlightsTool
from dotenv import load_dotenv


load_dotenv()

st.title("My Streamlit App")


model_id = st.sidebar.selectbox(
    "Model",
    (
        "gemini/gemini-2.5-pro-exp-03-25",
        "gemini/gemini-2.5-flash-preview-04-17",
        "gemini/gemini-2.0-flash",
    ),
    index=2,
)
max_steps = st.sidebar.number_input(
    "Max Steps",
    min_value=1,
    max_value=999,
    value=20,
    step=1,
)
planning_interval = st.sidebar.number_input(
    "Planning Interval",
    min_value=1,
    max_value=999,
    value=5,
    step=1,
)

model = LiteLLMModel(
    model_id=model_id,
    api_key=os.getenv("GOOGLE_API_KEY"),
)

search_agent = ToolCallingAgent(
    tools=[GoogleFlightsTool()],
    model=model,
    name="search_agent",
    description="Search for flights",
)

chat_agent = ToolCallingAgent(
    tools=[],
    model=model,
    name="chat_agent",
    description="Chat with the user",
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "agent" not in st.session_state:
    st.session_state.agent = CodeAgent(
        tools=[],
        model=model,
        max_steps=max_steps,
        planning_interval=planning_interval,
        managed_agents=[search_agent],
    )

# React to user input
prompt = st.chat_input("How can I help you?")
if prompt:
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = st.session_state.agent.run(
        prompt,
        reset=False,
    )
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
