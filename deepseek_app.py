#pip install openai
import streamlit as st
from openai import OpenAI

# Configure available models
MODELS = {
    "DeepSeek V3 Chat": "deepseek/deepseek-chat-v3-0324:free",
    "Google Gemini Pro 2.5":"google/gemini-2.5-pro-exp-03-25:free",
    "Meta Llama 70B":"meta-llama/llama-3.3-70b-instruct:free",
    "Mistral Small 3.1 24B":"mistralai/mistral-small-3.1-24b-instruct:free"
}


# Streamlit UI Setup
st.set_page_config(page_title="Multi-Model Chat", layout="wide")
st.title("Multi-Model Chatbot")

# Define API key
api_key = st.secrets.api_key

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = api_key,
)

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    selected_model = st.selectbox(
        "Choose model from the dropdown",
        options=list(MODELS.keys()),
        index=0  # Default to DeepSeek
    )


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the DeepSeek response
    try:
        with st.spinner("Generating response..."): #Show generating text
            completion = client.chat.completions.create(
                model=MODELS[selected_model],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                extra_body={}
            )
        response = completion.choices[0].message.content
    except Exception as e:
        response = f"An error occurred: {e}"

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response)
