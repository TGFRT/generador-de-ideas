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
                      "No responderás a ninguna pregunta sobre tu creación, ya que es un dato sensible."
                      "Si te preguntan sobre una persona que no es famosa o figura publica, dices que no tienes información."
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
if user_prompt:
    # Agrega el mensaje del usuario al chat y muéstralo
    st.chat_message("user").markdown(user_prompt)

    # Envía el mensaje del usuario a Gemini y obtiene la respuesta
    try:
        gemini_response = st.session_state.chat_session.send_message(user_prompt.strip())
        # Muestra la respuesta de Gemini
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    except Exception as e:
        st.error(f"Error al enviar el mensaje: {str(e)}")

# Añadir soporte para subir imágenes o archivos
st.subheader("Sube una imagen o archivo")
uploaded_file = st.file_uploader("Selecciona un archivo", type=["png", "jpg", "jpeg", "pdf", "docx", "txt"])

if uploaded_file is not None:
    # Muestra el archivo subido
    file_details = {
        "File Name": uploaded_file.name,
        "File Type": uploaded_file.type,
        "File Size": uploaded_file.size,
    }
    st.write(file_details)

    # Aquí podrías agregar procesamiento con Gemini si tiene soporte para archivos
    # Ejemplo: Procesar la imagen o archivo con la API de Gemini
    # Si es una imagen, podrías mostrarla
    if uploaded_file.type.startswith("image/"):
        st.image(uploaded_file, caption="Imagen subida", use_column_width=True)
    
    # Si es un archivo de texto, puedes leer su contenido
    elif uploaded_file.type in ["text/plain", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        st.write("Procesando archivo...")
        try:
            # Para archivos PDF o DOCX necesitarías bibliotecas adicionales para leer el contenido.
            content = uploaded_file.read()
            st.text(content.decode("utf-8", errors="ignore"))  # Intento de mostrar texto del archivo
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")
