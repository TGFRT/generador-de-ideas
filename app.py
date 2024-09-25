import streamlit as st
import requests
import json

# Configuración de la API de Gemini
GEMINI_API_URL = "https://api.gemini.example.com/analyze"  # Cambia esta URL por la correcta
API_KEY = "YOUR_GEMINI_API_KEY"  # Reemplaza con tu clave API de Gemini

# Función para analizar los datos del negocio con la API de Gemini
def analyze_business(data):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()  # Devuelve el análisis
    else:
        st.error("Error al comunicarse con la API de Gemini.")
        return None

# Interfaz de usuario
st.title("Analizador de Negocios con IA de Gemini")

# Recoger datos del negocio
with st.form("business_form"):
    st.subheader("Ingrese los datos de su negocio")
    ingresos = st.number_input("Ingresos mensuales (USD)", min_value=0)
    competencia = st.number_input("Número de competidores", min_value=0)
    cambio_mercado = st.checkbox("¿Hay cambios en el mercado?")

    submitted = st.form_submit_button("Analizar")
    if submitted:
        data = {
            'ingresos': ingresos,
            'competencia': competencia,
            'cambio_mercado': cambio_mercado
        }
        analysis_result = analyze_business(data)
        
        # Mostrar resultados
        if analysis_result:
            st.subheader("Resultados del Análisis")
            st.write(f"Etapa del negocio: **{analysis_result['stage']}**")
            st.write("Posibles amenazas:")
            st.write("- " + "\n- ".join(analysis_result.get('threats', ["Ninguna"])))
            st.write("Estrategias de marketing recomendadas:")
            st.write("- " + "\n- ".join(analysis_result.get('marketing_strategies', [])))

