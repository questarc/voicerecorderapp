import io
import uuid
from datetime import datetime

import streamlit as st
from audio_recorder_streamlit import audio_recorder
from pydub import AudioSegment


def save_audio_to_wav(audio_bytes: bytes, filename: str) -> bytes:
    """
    Convert raw audio bytes (usually webm/ogg from the component)
    into a WAV file in memory and return the WAV bytes.
    """
    # Load from bytes (pydub auto-detects format in many cases)
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

    # Export to WAV in memory
    wav_buffer = io.BytesIO()
    audio.export(wav_buffer, format="wav")
    wav_buffer.seek(0)
    return wav_buffer.read()


def main():
    st.set_page_config(
        page_title="Production-Grade Voice Recorder",
        page_icon="🎙️",
        layout="centered",
    )

    st.title("🎙️ Voice Recorder")
    st.caption("Record your voice, preview it, and download as an audio file.")

    # Sidebar configuration / metadata
    with st.sidebar:
        st.header("Recording Settings")
        default_filename_prefix = st.text_input(
            "File name prefix",
            value="recording",
            help="This will be used as the base name for your downloaded file.",
        )
        add_timestamp = st.checkbox(
            "Append timestamp to file name", value=True
        )
        st.markdown("---")
        st.markdown("**Tips**")
        st.markdown(
            "- Click the microphone to start/stop recording.\n"
            "- Wait for processing before downloading.\n"
            "- Use a modern browser (Chrome, Edge, etc.)."
        )

    st.subheader("Step 1: Record your voice")

    # The audio recorder component
    audio_bytes = audio_recorder(
        text="Click to start / stop recording",
        recording_color="#e74c3c",
        neutral_color="#2ecc71",
        icon_name="microphone",
        icon_size="3x",
    )

    if audio_bytes:
        st.success("Recording captured successfully!")

        # Show basic info
        st.subheader("Step 2: Preview your recording")
        st.audio(audio_bytes, format="audio/webm")

        # Convert to WAV for download (more universally supported)
        try:
            wav_bytes = save_audio_to_wav(audio_bytes, "temp.wav")
        except Exception as e:
            st.error(f"Error converting audio: {e}")
            st.stop()

        # Generate filename
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{default_filename_prefix}_{timestamp}.wav"
        else:
            # Add a short random suffix to avoid collisions
            suffix = uuid.uuid4().hex[:6]
            filename = f"{default_filename_prefix}_{suffix}.wav"

        st.subheader("Step 3: Download your file")
        st.download_button(
            label="⬇️ Download recording as WAV",
            data=wav_bytes,
            file_name=filename,
            mime="audio/wav",
        )

        # Optional: show some metadata / debug info
        with st.expander("Advanced info"):
            st.write("**Raw bytes length:**", len(audio_bytes))
            st.write("**WAV bytes length:**", len(wav_bytes))
            st.write("**Suggested filename:**", filename)
    else:
        st.info("No recording yet. Click the microphone above to start.")


if __name__ == "__main__":
    main()
