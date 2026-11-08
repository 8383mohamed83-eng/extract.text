import streamlit as st
from groq import Groq
import os , tempfile

st.title("استخراج النص")

st.subheader("رفع ملف فيديو أو صوت")

st.write("ارفع فيديو أو ملف صوتي")

client = Groq(api_key=st.secrets["API_SEC"])

def transcribe_audio_file(path):
    with open(path, "rb") as f:
        transcribe = client.audio.transcriptions.create(
            model='whisper-large-v3',
            file=(os.path.basename(path),f),
            response_format="text"
        )

    return transcribe

uploaded_file = st.file_uploader("upload your vidoe",type=["mp4", "mp3", "wav", "m4a", "ogg", "webm"])

if uploaded_file:
    if uploaded_file.size / 1024**2 > 25:
        st.error("the file must be less than 25 MB")
    elif st.button("Extract", key="file_btn"):
        with st.spinner("extracting..."):
            ext = os.path.splitext(uploaded_file.name)[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(uploaded_file.read())
                path = tmp.name
            try:
                transcript = transcribe_audio_file(path)
            finally:
                os.unlink(path)

        if not transcript or len (transcript.split()) < 5 :
            st.error("there is no text")
        else :
            st.subheader("EXTRACTED TEXT")
            st.write(transcript)
            st.download_button("download",transcript,file_name="text.txt")
