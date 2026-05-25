import streamlit as st
import streamlit.components.v1 as components

st.title("🎙️ Voice Recorder (no backend wiring yet)")

components.html(
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
            status.innerText = "Status: Stopped";
            // On this Streamlit setup we can't send data back to Python reliably.
        };

        recorder.start();
    };

    stopBtn.onclick = () => {
        recorder.stop();
    };
    </script>
    """,
    height=250,
)
