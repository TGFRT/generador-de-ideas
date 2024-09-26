import streamlit as st
import google.generativeai as gen_ai

# Configura Streamlit
st.set_page_config(
    page_title="Generador de Ideas de Negocio - IngenIAr",
    page_icon=":lightbulb:",
    layout="centered",
)

# Obtén la clave API de las variables de entorno
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configura el modelo de Google Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Configuración de generación
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

# Título de la web
st.title("Generador de Ideas de Negocio 💡")

# Sección de información del usuario
st.header("Cuéntanos sobre ti")

# Cajas de texto para ingresar información del usuario
intereses = st.text_area("¿Cuáles son tus intereses o pasiones?")
experiencia = st.text_area("¿Cuál es tu experiencia laboral o académica?")
conocimientos = st.text_area("¿En qué áreas tienes conocimientos o habilidades?")
mercado = st.text_area("¿Qué tipo de mercado te interesa?")
problemas = st.text_area("¿Qué problemas o necesidades quieres resolver?")

# Botón para iniciar la generación de ideas
if st.button("Generar Ideas"):
    # Validación de entradas
    if not (intereses and experiencia and conocimientos and mercado and problemas):
        st.error("Por favor, completa todos los campos antes de generar ideas.")
    else:
        # Crea el prompt para la API de Gemini
        prompt = f"""
        Genera 5 ideas de negocio innovadoras para una persona con las siguientes características:
        - Intereses: {intereses}
        - Experiencia: {experiencia}
        - Conocimientos: {conocimientos}
        - Mercado: {mercado}
        - Problemas a resolver: {problemas}
        
        Incluye una breve descripción de cada idea y su potencial mercado.
        """

        # Envía el prompt a Gemini para obtener las ideas
        try:
            # Crea el modelo de generación
            model = gen_ai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="Eres un generador de ideas de negocio innovadoras. "
                                  "Proporciona ideas creativas basadas en la información proporcionada."
            )

            # Inicializa la sesión de chat
            chat_session = model.start_chat(history=[])

            # Envía el mensaje al modelo y obtiene la respuesta
            gemini_response = chat_session.send_message(prompt)

            # Muestra las ideas al usuario
            st.markdown(f"## Ideas de negocio:\n{gemini_response.text}")
        except Exception as e:
            st.error(f"Ocurrió un error al generar las ideas: {str(e)}")
