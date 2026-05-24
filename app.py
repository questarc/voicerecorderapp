import streamlit as st
import streamlit.components.v1 as components
import base64

st.title("🎙️ Voice Recorder (Stable & Streamlit‑Cloud Compatible)")

# --- Component wrapper ---
def voice_recorder():
    value = components.html(
        """
        <div>
            <button id="startBtn">Start Recording</button>
            <button id="stopBtn">Stop Recording</button>
        </div>

        <script>
        let recorder;
        let chunks = [];

        async function startRecording() {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            recorder = new MediaRecorder(stream);
            recorder.ondataavailable = e => chunks.push(e.data);
            recorder.onstop = e => {
                const blob = new Blob(chunks, { type: "audio/webm" });
                chunks = [];
                const reader = new FileReader();
                reader.onloadend = () => {
                    const base64data = reader.result.split(",")[1];
                    Streamlit.setComponentValue(base64data);
                };
                reader.readAsDataURL(blob);
            };
            recorder.start();
        }

        function stopRecording() {
            recorder.stop();
        }

        document.getElementById("startBtn").onclick = startRecording;
        document.getElementById("stopBtn").onclick = stopRecording;
        </script>
        """,
        height=200,
    )
    return value


# --- Get audio from component ---
audio_base64 = voice_recorder()

# --- If audio exists, decode and display ---
if isinstance(audio_base64, str) and len(audio_base64) > 0:
    audio_bytes = base64.b64decode(audio_base64)
    st.audio(audio_bytes, format="audio/webm")
    st.download_button("Download Recording", audio_bytes, "recording.webm")
