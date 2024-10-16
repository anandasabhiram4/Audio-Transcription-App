import os
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

# Set ffmpeg and ffprobe paths
os.environ["PATH"] += os.pathsep + '/opt/homebrew/bin'
AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"
AudioSegment.ffmpeg = "/opt/homebrew/bin/ffmpeg"
AudioSegment.ffprobe = "/opt/homebrew/bin/ffprobe"

# Function to transcribe audio
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        try:
            audio_data = recognizer.record(source)
            st.write("Successfully recorded audio data.")  # Debugging line
        except Exception as e:
            st.error(f"Error recording audio: {e}")
            return None

        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Streamlit application layout
st.title("Audio Transcription App")
st.write("Upload an audio file to transcribe it into text.")

# File uploader for audio files
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    # Save the uploaded audio file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name

    # Convert to WAV if necessary
    audio_file_to_use = temp_file_path  # Default to the uploaded file path
    if uploaded_file.name.endswith('.mp3'):
        try:
            audio = AudioSegment.from_mp3(temp_file_path)
            temp_wav_path = temp_file_path.replace('.mp3', '.wav')
            audio.export(temp_wav_path, format='wav')
            audio_file_to_use = temp_wav_path
            st.write("Converted MP3 to WAV format.")  # Debugging line
        except Exception as e:
            st.error(f"Error converting MP3 to WAV: {e}")
            audio_file_to_use = None

    if audio_file_to_use:
        st.audio(audio_file_to_use, format='audio/wav')

        # Button to trigger transcription
        if st.button("Transcribe"):
            transcription = transcribe_audio(audio_file_to_use)
            st.write("Transcription: ", transcription)
