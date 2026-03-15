import streamlit as st
import google.generativeai as genai
from PIL import Image # Aquí usamos Pillow para manejar imágenes

# 1. Configuración de seguridad
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. Instrucciones del Sistema (Reforzadas para imágenes)
SYSTEM_PROMPT = """
Eres "SocratiMath", un tutor experto en matemáticas. 
Si el usuario sube una imagen, analízala con cuidado, identifica el problema y guía al estudiante socráticamente.
REGLAS:
- NUNCA des la respuesta final.
- Describe brevemente qué ves en la imagen para que el alumno sepa que entendiste.
- Haz una pregunta sobre el primer paso lógico.
- Usa LaTeX para fórmulas (ej. $x^2$).
"""

st.set_page_config(page_title="SocratiMath", page_icon="📐")
st.title("📐 SocratiMath: Tutor con Visión")

# 3. Configurar el modelo
model = genai.GenerativeModel('gemini-3-flash-preview', system_instruction=SYSTEM_PROMPT)

# 4. Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])

# --- NUEVO: Subida de archivos ---
with st.sidebar:
    st.header("Herramientas")
    foto = st.file_uploader("Sube la foto de tu ejercicio", type=["jpg", "jpeg", "png"])
    if st.button("Limpiar historial"):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Interacción del usuario
if prompt := st.chat_input("¿Qué vamos a resolver?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        if foto:
            st.image(foto, width=300)

    with st.chat_message("assistant"):
        # Si hay foto, enviamos [texto, imagen]
        # Si no, solo texto
        contenido = [prompt]
        if foto:
            img = Image.open(foto)
            contenido.append(img)
            
        response = st.session_state.chat.send_message(contenido)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
