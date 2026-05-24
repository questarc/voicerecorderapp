import streamlit as st
import streamlit.components.v1 as components
import base64

st.title("🎙️ Voice Recorder (Python 3.14 Compatible)")

# HTML + JS recorder
audio_component = components.html(
    """
    <html>
    <body>
    <button onclick="startRecording()">Start Recording</button>
    <button onclick="stopRecording()">Stop Recording</button>

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
                const streamlitEvent = new Event("streamlit:audio");
                streamlitEvent.data = base64data;
                window.parent.document.dispatchEvent(streamlitEvent);
            };
            reader.readAsDataURL(blob);
        };
        recorder.start();
    }

    function stopRecording() {
        recorder.stop();
    }
    </script>
    </body>
    </html>
    """,
    height=200,
)

# Listen for JS → Python events
audio_state = st.session_state.get("audio_data")

def js_event_listener():
    """Registers a JS event listener inside Streamlit."""
    components.html(
        """
        <script>
        document.addEventListener("streamlit:audio", (e) => {
            const data = e.data;
            window.parent.postMessage({type: "audio", data: data}, "*");
        });
        </script>
        """,
        height=0,
    )

js_event_listener()

# Receive postMessage events
message = st.experimental_get_websocket_message()

if message and message.get("type") == "audio":
    st.session_state["audio_data"] = message["data"]
    audio_state = message["data"]

# If we have audio, show it
if audio_state:
    audio_bytes = base64.b64decode(audio_state)
    st.audio(audio_bytes, format="audio/webm")
    st.download_button("Download Recording", audio_bytes, "recording.webm")
