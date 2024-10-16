import os
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

# Set ffmpeg and ffprobe paths
ffmpeg_path = '/opt/homebrew/bin/ffmpeg'
ffprobe_path = '/opt/homebrew/bin/ffprobe'

# Check if ffmpeg and ffprobe are installed
if not os.path.isfile(ffmpeg_path) or not os.path.isfile(ffprobe_path):
    st.error("FFmpeg or ffprobe not found. Please check your installation.")
else:
    AudioSegment.converter = ffmpeg_path
    AudioSegment.ffmpeg = ffmpeg_path
    AudioSegment.ffprobe = ffprobe_path

# Function to transcribe audio
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
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

    st.write(f"Temporary file created at: {temp_file_path}")  # Debug output

    # Convert to WAV if necessary
    if uploaded_file.name.endswith('.mp3'):
        try:
            audio = AudioSegment.from_mp3(temp_file_path)
            temp_wav_path = temp_file_path.replace('.mp3', '.wav')
            audio.export(temp_wav_path, format='wav')
            audio_file_to_use = temp_wav_path
            st.write(f"Converted MP3 to WAV at: {audio_file_to_use}")  # Debug output
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