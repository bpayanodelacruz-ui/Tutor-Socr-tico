import streamlit as st
import google.generativeai as genai

# 1. Configuración de seguridad: Leemos la clave desde los Secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. Instrucciones del Sistema (Tu método socrático)
SYSTEM_PROMPT = """
Eres "SocratiMath", un tutor experto en matemáticas que usa el método socrático.
NUNCA des la respuesta final. Tu objetivo es guiar al estudiante con preguntas.
REGLAS:
- Si el usuario te da un problema, identifica el primer paso y haz una pregunta sobre él.
- Usa LaTeX para fórmulas (ej. $x^2$).
- Si el usuario se equivoca, ayúdale a ver el error con otra pregunta.
- Sé breve y motivador.
"""

st.set_page_config(page_title="SocratiMath", page_icon="📐")
st.title("📐 SocratiMath Tutor")
st.markdown("---")

# 3. Configurar el modelo
model = genai.GenerativeModel('gemini-3-flash-preview', system_instruction=SYSTEM_PROMPT)

# 4. Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Interacción del usuario
if prompt := st.chat_input("¿En qué ejercicio puedo ayudarte hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
