import streamlit as st
import requests

st.set_page_config(page_title="Agente Virtual com IA", layout="centered")

st.title("Agente Virtual com IA")
st.markdown(
    "Converse com modelos avançados como Groq LLaMA3 e GPT-4, com busca opcional."
)

# Sidebar form for input configuration
with st.sidebar:
    st.header("Configure o Agente")

    model_provider = st.selectbox("Selecione o Modelo", ["Groq", "OpenAI"])

    model_name = st.selectbox("Modelo de IA", ["llama3-70b-8192", "gpt-4o-mini"])

    system_prompt = st.text_area(
        "Prompt para instrução",
        value="Seja um assistente de IA eficiente, simpático e com respostas precisas.",
        height=100,
    )

    allow_search = st.checkbox("Habilitar busca na web", value=False)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(msg)
    else:
        with st.chat_message("ai"):
            st.markdown(msg)

# Handle user input
user_query = st.chat_input("Digite sua mensagem...")

if user_query:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.chat_history.append(("user", user_query))

    # Send request to FastAPI backend
    with st.chat_message("ai"):
        with st.spinner("Pensando..."):
            try:
                payload = {
                    "model_name": model_name,
                    "model_provider": model_provider,
                    "system_prompt": system_prompt,
                    "messages": [user_query],
                    "allow_search": allow_search,
                }
                res = requests.post("http://localhost:8000/chat", json=payload)
                response = res.json()
                st.markdown(response)
                st.session_state.chat_history.append(("ai", response))
            except Exception as e:
                st.error(f"Error: {e}")
