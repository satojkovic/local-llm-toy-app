import streamlit as st
import os
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from phi.tools.yfinance import YFinanceTools

def get_assistant(tools):
    return Assistant(
        name="llama3 assistant",
        llm=Ollama(model='llama3'),
        tools=tools,
        description='You are a helpful assistant that can access specific tools based on user selection.',
        show_tool_calls=True,
        debug_mode=True,
        add_datetime_to_instructions=True,
    )

st.set_page_config(page_title='Llama tool use')

# App settings
st.title("local llama3 tool use")
st.markdown(
    'this app demonstrates function calling with the local llama3 model using ollama. select tools in the sidebar and ask relevant questions'
)

# Sidebar
st.sidebar.title('tool selection')
use_yfinance = st.sidebar.checkbox('yfinance (stock data)', value=True)

tools = []
if use_yfinance:
    tools.append(YFinanceTools(stock_price=True, company_info=True))

# Initialize or update the assistant
if "assistant" not in st.session_state or st.session_state.get('tools') != tools:
    st.session_state.assistant = get_assistant(tools)
    st.session_state.tools = tools
    st.session_state.messages = []

# Display current tool status and chat interface
st.sidebar.markdown('### Current tools:')
st.sidebar.markdown(f'- yfinance: {"Enabled" if use_yfinance else "Disabled"}')

for message in st.session_state.get('messages', []):
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Implement chat input and response generation
if prompt := st.chat_input('ask a question based on the enabled tools'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        response_container = st.empty()
        response = ''
        for chunk in st.session_state.assistant.run(prompt):
            response += chunk
            response_container.write(response + '| ')
        response_container.write(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
