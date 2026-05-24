import streamlit as st
import streamlit.components.v1 as components
import base64

st.title("🎙️ Voice Recorder (Reliable Streamlit Component)")

# --- Component wrapper ---
def recorder_component():
    return components.html(
        """
        <div style="font-family: sans-serif;">
            <button id="startBtn">🎤 Start Recording</button>
            <button id="stopBtn" disabled>⏹ Stop Recording</button>
            <p id="status">Status: Idle</p>
        </div>

        <script>
        let recorder;
        let chunks = [];

        const startBtn = document.getElementById("startBtn");
        const stopBtn = document.getElementById("stopBtn");
        const status = document.getElementById("status");

        startBtn.onclick = async () => {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            recorder = new MediaRecorder(stream);

            chunks = [];
            recorder.ondataavailable = e => chunks.push(e.data);

            recorder.onstart = () => {
                status.innerText = "Status: Recording...";
                startBtn.disabled = true;
                stopBtn.disabled = false;
            };

            recorder.onstop = () => {
                status.innerText = "Status: Processing...";
                const blob = new Blob(chunks, { type: "audio/webm" });
                const reader = new FileReader();
                reader.onloadend = () => {
                    const base64data = reader.result.split(",")[1];
                    Streamlit.setComponentValue(base64data);
                };
                reader.readAsDataURL(blob);

                startBtn.disabled = false;
                stopBtn.disabled = true;
            };

            recorder.start();
        };

        stopBtn.onclick = () => {
            recorder.stop();
            status.innerText = "Status: Stopped";
        };
        </script>
        """,
        height=250,
    )


# --- Get audio from component ---
audio_base64 = recorder_component()

# --- If audio exists, decode and display ---
if isinstance(audio_base64, str) and audio_base64.strip():
    audio_bytes = base64.b64decode(audio_base64)
    st.success("Recording complete!")
    st.audio(audio_bytes, format="audio/webm")
    st.download_button("Download Recording", audio_bytes, "recording.webm")
