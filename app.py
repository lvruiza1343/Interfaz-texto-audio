import streamlit as st
import os
import time
import glob
import base64
from gtts import gTTS
from PIL import Image

# Configuración inicial
st.set_page_config(page_title="Texto a Audio", page_icon="🎵", layout="centered")
st.title("🎶 Conversión de Texto a Audio 🎶")

# Imagen principal
image = Image.open('gato_raton.png')  # Asegúrate de tener esta imagen
st.image(image, width=300)

# Sidebar
with st.sidebar:
    st.header("📝 Opciones")
    st.markdown("Escribe o selecciona un texto para convertirlo en audio 🎧")

# Crear carpeta temporal si no existe
if not os.path.exists("temp"):
    os.makedirs("temp")

# Cuento corto
st.subheader("✨ Un cuento corto ✨")
st.write(
    """
    Hace mucho tiempo, en un pequeño pueblo rodeado de montañas, vivía una niña que soñaba con tocar las estrellas.
    Cada noche subía a la colina más alta y extendía sus manos hacia el cielo. Un día, una estrella fugaz cayó
    frente a ella, convirtiéndose en una pequeña luz danzante. Desde entonces, nunca dejó de soñar, y el pueblo entero
    aprendió que los sueños, a veces, bajan a saludarnos.
    """
)

# Entrada de texto
st.markdown("¿Quieres escucharlo? 🎤 Copia o escribe tu propio texto:")
text = st.text_area("✏️ Ingrese el texto a convertir en audio:")

# Selección de idioma
option_lang = st.selectbox(
    "🌐 Selecciona el idioma:",
    ("Español", "Inglés")
)
lg = 'es' if option_lang == "Español" else 'en'

# Función de conversión de texto a audio
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    file_name = text[0:20].strip().replace(" ", "_") or "audio"
    file_path = f"temp/{file_name}.mp3"
    tts.save(file_path)
    return file_name, file_path

# Botón para convertir
if st.button("🎙️ Convertir a Audio"):
    if text.strip() == "":
        st.warning("⚠️ Por favor, ingresa algún texto para convertir.")
    else:
        result_name, audio_path = text_to_speech(text, lg)
        st.success("✅ ¡Audio generado exitosamente!")
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Botón de descarga
        with open(audio_path, "rb") as f:
            data = f.read()

        def get_binary_file_downloader_html(bin_data, filename='audio.mp3', file_label='Descargar Audio'):
            bin_str = base64.b64encode(bin_data).decode()
            href = f'<a href="data:audio/mp3;base64,{bin_str}" download="{filename}" style="color: white; background-color: #4CAF50; padding: 8px 16px; text-decoration: none; border-radius: 5px;">{file_label}</a>'
            return href

        st.markdown(get_binary_file_downloader_html(data, filename=os.path.basename(audio_path)), unsafe_allow_html=True)

# Función para eliminar audios viejos
def remove_old_files(days=7):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    cutoff = now - (days * 86400)
    for file in mp3_files:
        if os.path.getmtime(file) < cutoff:
            os.remove(file)
            print("Deleted:", file)

remove_old_files()

