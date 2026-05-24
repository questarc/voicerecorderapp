import streamlit as st
import base64
import streamlit.components.v1 as components

st.title("🎙️ Voice Recorder (Fully Streamlit‑Compatible)")

# Component wrapper
def audio_recorder():
    component_value = components.html(
        """
        <script>
        const startBtn = document.createElement("button");
        startBtn.innerText = "Start Recording";
        const stopBtn = document.createElement("button");
        stopBtn.innerText = "Stop Recording";

        document.body.appendChild(startBtn);
        document.body.appendChild(stopBtn);

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

        startBtn.onclick = startRecording;
        stopBtn.onclick = stopRecording;
        </script>
        """,
        height=200,
    )
    return component_value


audio_data = audio_recorder()

if audio_data:
    audio_bytes = base64.b64decode(audio_data)
    st.audio(audio_bytes, format="audio/webm")
    st.download_button("Download Recording", audio_bytes, "recording.webm")
