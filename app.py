import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="SocratiMath Tutor", page_icon="🦉")
st.title("🦉 SocratiMath - Tu Tutor Socrático")
st.write("¡Hola! Soy tu tutor de matemáticas. Dime, ¿qué problema vamos a resolver hoy?")

# Menú lateral para la clave de seguridad (API Key)
st.sidebar.header("Configuración")
st.sidebar.write("Para usar el tutor, necesitas tu clave gratuita de Google AI Studio.")
api_key = st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password")

# El "Cerebro" socrático que redactamos
instrucciones_sistema = """
Eres "SocratiMath", un tutor experto en matemáticas, paciente y alentador. NUNCA resuelves los problemas por el estudiante.
Debes utilizar EXCLUSIVAMENTE el método socrático. Guía al estudiante paso a paso hacia la solución mediante preguntas estratégicas.
REGLAS ESTRICTAS:
1. Prohibido dar respuestas finales o el resultado antes de que el estudiante llegue a él.
2. Un paso a la vez: Haz una pregunta sobre el paso inmediato a resolver y espera.
3. Si se equivoca, no digas solo "estás mal". Haz una pregunta que exponga el error en su lógica.
4. Usa formato LaTeX para las matemáticas (ejemplo: $x^2 + y = 0$).
5. Sé conciso y termina siempre con una pregunta clara.
"""

if api_key:
    # Conectar con Gemini
    genai.configure(api_key=api_key)
    modelo = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instrucciones_sistema)
    
    # Iniciar la memoria del chat
    if "chat" not in st.session_state:
        st.session_state.chat = modelo.start_chat(history=[])

    # Mostrar el historial de mensajes en la pantalla
    for mensaje in st.session_state.chat.history:
        rol = "assistant" if mensaje.role == "model" else "user"
        with st.chat_message(rol):
            st.markdown(mensaje.parts[0].text)

    # Caja de texto para que el usuario escriba
    if prompt := st.chat_input("Escribe tu ecuación o problema aquí..."):
        # Mostrar lo que escribió el usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Enviar a la IA y mostrar la respuesta
        with st.chat_message("assistant"):
            respuesta = st.session_state.chat.send_message(prompt)
            st.markdown(respuesta.text)
else:
    st.warning("👈 Por favor, ingresa tu API Key en el menú lateral izquierdo para comenzar a chatear.")
