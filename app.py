import streamlit as st
import base64

st.title("🎙️ Voice Recorder (Python 3.14 Compatible)")

st.markdown("""
<script>
let chunks = [];
let recorder;

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = e => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        chunks = [];
        const reader = new FileReader();
        reader.onloadend = () => {
            const base64data = reader.result.split(',')[1];
            window.parent.postMessage({ type: 'audio', data: base64data }, '*');
        };
        reader.readAsDataURL(blob);
    };
    recorder.start();
}

function stopRecording() {
    recorder.stop();
}
</script>

<button onclick="startRecording()">Start Recording</button>
<button onclick="stopRecording()">Stop Recording</button>
""", unsafe_allow_html=True)

# Receive audio from JS
audio_data = st.experimental_get_query_params().get("audio", None)

if audio_data:
    audio_bytes = base64.b64decode(audio_data[0])
    st.audio(audio_bytes, format="audio/webm")
    st.download_button("Download Recording", audio_bytes, "recording.webm")
