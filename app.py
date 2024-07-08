import io
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pygame
from googletrans import Translator

# Initialize the speech recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Initialize pygame mixer for playing audio
pygame.mixer.init()

def record_audio():
    with sr.Microphone() as source:
        st.write("Please speak now or enter text below...")
        audio = recognizer.listen(source)
        try:
            st.write("Recognizing...")
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
    return None

def translate_text(text, target_language):
    translation = translator.translate(text, dest=target_language)
    st.write(f"Translated text: {translation.text}")
    return translation.text

def text_to_speech(text, language):
    tts = gTTS(text=text, lang=language)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.mixer.music.load(mp3_fp)
    pygame.mixer.music.play()

st.title("BhashaLink")

# Define the language options
indian_languages = {
    "Hindi": "hi",
    "Bengali": "bn",
    "Telugu": "te",
    "Marathi": "mr",
    "Tamil": "ta",
    "Kannada": "kn",
    "English": "en"
}

# UI elements for language selection
source_language = st.selectbox("Select Source Language:", list(indian_languages.keys()))
target_language = st.selectbox("Select Target Language:", list(indian_languages.keys()))

source_language_code = indian_languages[source_language]
target_language_code = indian_languages[target_language]

# Option to choose input method (text or speech)
input_method = st.radio("Choose Input Method:", ("Text Input", "Speech Input"))

if input_method == "Text Input":
    input_text = st.text_input("Enter Text:", "")
    if st.button("Translate and Speak"):
        if input_text:
            # Translate text
            translated_text = translate_text(input_text, target_language_code)
            # Convert translated text to speech
            text_to_speech(translated_text, target_language_code)
        else:
            st.write("Please enter some text.")
elif input_method == "Speech Input":
    if st.button("Start Recording"):
        # Record audio
        input_text = record_audio()
        if input_text:
            # Translate text
            translated_text = translate_text(input_text, target_language_code)
            # Convert translated text to speech
            text_to_speech(translated_text, target_language_code)

if st.button("Stop"):
    pygame.mixer.music.stop()