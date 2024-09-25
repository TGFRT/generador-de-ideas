import streamlit as st
import requests
import json
import os

# Obtener la clave API desde la variable de entorno
API_KEY = os.getenv('GOOGLE_API_KEY')

# Configuración de la API de Gemini
GEMINI_API_URL = "https://api.gemini.example.com/analyze"  # Cambia esta URL por la correcta

# Función para analizar los datos del negocio con la API de Gemini
def analyze_business(data):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx
        return response.json()  # Devuelve el análisis
    except requests.exceptions.RequestException as e:
        st.error(f"Error en la conexión: {e}")
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
