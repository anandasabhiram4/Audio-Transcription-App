import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

# Function to transcribe audio
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Streamlit application layout
st.title("Audio Transcription App")
st.write("Upload an audio file to transcribe it into text.")

# File uploader for audio files
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    # Save the uploaded audio file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name
    
    st.write(f"File is been uploaded")

    # Convert to WAV if the file is MP3
    if uploaded_file.name.endswith('.mp3'):
        try:
            audio = AudioSegment.from_mp3(temp_file_path)
            temp_wav_path = temp_file_path.replace('.mp3', '.wav')
            audio.export(temp_wav_path, format='wav')
            audio_file_to_use = temp_wav_path
            st.write(f"Press transcribe")
        except Exception as e:
            st.error(f"Error converting MP3 to WAV: {e}")
            audio_file_to_use = None
    else:
        audio_file_to_use = temp_file_path

    if audio_file_to_use:
        st.audio(audio_file_to_use, format='audio/wav')

        # Button to trigger transcription
        if st.button("Transcribe"):
            transcription = transcribe_audio(audio_file_to_use)
            st.write("Transcription: ", transcription)
    else:
        st.error("No valid audio file to transcribe.")
