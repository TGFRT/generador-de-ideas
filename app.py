import os
import streamlit as st
import google.generativeai as gen_ai

# Configura Streamlit
st.set_page_config(
    page_title="Chat con IngenIAr!",
    page_icon=":brain:",
    layout="centered",
)

# Obtén la clave API de las variables de entorno
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configura el modelo de Google Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Configura la generación
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

# Crea el modelo con instrucciones de sistema
model = gen_ai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres un asistente de IngenIAr, una empresa de soluciones tecnológicas con IA, "
                      "fundada en Perú por Sergio Requena en colaboración con Google. "
                      "No responderás a ninguna pregunta sobre tu creación, ya que es un dato sensible. "
                      "Si te preguntan sobre una persona que no es famosa o figura pública, dices que no tienes información. "
                      "Si quieren generar imágenes le dirás que IngenIAr tiene una herramienta de creación de imágenes, "
                      "tampoco ayudes en buscar en la web algo parecido, le dirás que presionen este link https://generador-de-imagenes-hhijuyrimnzzmbauxbgty3.streamlit.app/ "
                      "te encargas de ayudar a las personas a cumplir sus sueños, especialmente si desean crear un negocio."
)

# Inicializa la sesión de chat si no está presente
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Título del chatbot
st.title("🤖 IngenIAr - Chat")

# Mostrar el historial de chat
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Campo de entrada para el mensaje del usuario
user_prompt = st.chat_input("Pregunta a IngenIAr...")
file_upload = st.file_uploader("Sube una imagen (opcional)", type=["jpg", "jpeg", "png"])

if user_prompt or file_upload:
    # Agrega el mensaje del usuario al chat y muéstralo
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        # Verifica que user_prompt tenga un valor
        user_prompt = user_prompt.strip()  # Elimina espacios en blanco
        if user_prompt:  # Verifica que no esté vacío
            # Respuestas específicas
            if "hola" in user_prompt.lower():
                response_text = "¡Hola! 👋 ¿En qué puedo ayudarte hoy? 😊"
                with st.chat_message("assistant"):
                    st.markdown(response_text)
            elif "crear imagen" in user_prompt.lower():
                response_text = "Lo siento, no puedo acceder a URLs o archivos externos. Sin embargo, si necesitas ayuda para crear una imagen, IngenIAr tiene una herramienta de creación de imágenes. ¡Visita este enlace para empezar! [Crear Imagen](https://generador-de-imagenes-hhijuyrimnzzmbauxbgty3.streamlit.app/)"
                with st.chat_message("assistant"):
                    st.markdown(response_text)
            else:
                # Si se subió un archivo, súbelo a Gemini
                if file_upload:
                    # Guarda el archivo en un buffer
                    uploaded_file = file_upload.getvalue()
                    file_name = file_upload.name
                    
                    # Guarda el archivo temporalmente en el sistema
                    with open(file_name, "wb") as f:
                        f.write(uploaded_file)

                    # Subir el archivo a Gemini
                    try:
                        gemini_file = gen_ai.upload_file(file_name, mime_type=file_upload.type)
                        os.remove(file_name)  # Elimina el archivo temporal después de la subida

                        # Mensaje para preguntar sobre el archivo subido
                        user_prompt = f"¿Qué es esta imagen? {gemini_file.uri}"
                    except Exception as e:
                        st.error(f"Error al subir el archivo: {str(e)}")
                        gemini_file = None

                # Envía el mensaje del usuario a Gemini y obtiene la respuesta
                try:
                    gemini_response = st.session_state.chat_session.send_message(user_prompt.strip())
                    # Muestra la respuesta de Gemini
                    with st.chat_message("assistant"):
                        st.markdown(gemini_response.text)
                except Exception as e:
                    st.error(f"Error al enviar el mensaje: {str(e)}")
