import streamlit as st
from typing import Optional, Dict
import tempfile
import os

class VoiceProcessor:
    def __init__(self, model_name: str = "tiny"):
        """
        Initialize the VoiceProcessor with a specified Whisper model.
        
        Args:
            model_name (str): Whisper model to use ('tiny', 'base', 'small', etc.). Default is 'tiny' for efficiency.
        """
        self.model = None
        self.model_name = model_name
        st.info(f"🎤 VoiceProcessor initialized. Whisper model '{model_name}' will load when needed.")

    def load_whisper_model(self) -> bool:
        """
        Load the Whisper model if not already loaded.
        
        Returns:
            bool: True if model loaded successfully, False otherwise.
        """
        if self.model is None:
            try:
                import whisper
                with st.spinner(f"Loading Whisper model '{self.model_name}'... This may take a moment."):
                    self.model = whisper.load_model(self.model_name)
                st.success(f"✅ Whisper '{self.model_name}' model loaded successfully!")
                return True
            except Exception as e:
                st.error(f"❌ Error loading Whisper model: {str(e)}")
                st.info("💡 Ensure 'openai-whisper' is installed: `pip install openai-whisper`")
                st.info("💡 Also, ensure 'ffmpeg' is installed for audio processing.")
                return False
        return True

    def transcribe_audio(self, audio_data: bytes, filename: str = "temp_audio.wav") -> Optional[Dict]:
        """
        Transcribe audio data to text using Whisper.
        
        Args:
            audio_data (bytes): Raw audio data (e.g., from file upload).
            filename (str): Name of the audio file (used for extension detection). Default is 'temp_audio.wav'.
        
        Returns:
            Optional[Dict]: Dictionary with 'text' (transcribed text) and 'language' (detected language),
                           or None if transcription fails.
        """
        if not self.load_whisper_model():
            return None

        try:
            # Create a temporary file to store audio data
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
                tmp_file.write(audio_data)
                tmp_file.flush()
                temp_path = tmp_file.name

            # Verify temporary file
            if not os.path.exists(temp_path):
                st.error("❌ Temporary audio file not created")
                return None

            file_size = os.path.getsize(temp_path)
            if file_size == 0:
                st.error("❌ Temporary audio file is empty")
                os.unlink(temp_path)
                return None

            st.info(f"📊 Processing audio file (size: {file_size} bytes) at {temp_path}")

            # Transcribe audio using Whisper
            with st.spinner("🤖 Transcribing audio..."):
                result = self.model.transcribe(temp_path, language=None)  # Auto-detect language

            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except Exception as e:
                st.warning(f"⚠️ Could not delete temporary file: {str(e)}")

            # Process transcription result
            if result and 'text' in result and result['text'].strip():
                st.success("✅ Audio transcribed successfully!")
                return {
                    'text': result['text'].strip(),
                    'language': result.get('language', 'unknown')
                }
            else:
                st.error("❌ No speech detected in audio")
                st.info("💡 Ensure the audio contains clear speech and is in a supported format (WAV, MP3, M4A)")
                return None

        except Exception as e:
            st.error(f"❌ Error transcribing audio: {str(e)}")
            st.info("💡 Try using a different audio file or check audio format compatibility")
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            except:
                pass
            return None

if __name__ == "__main__":
    # Example usage for testing
    import sys
    if 'streamlit' in sys.modules:
        st.write("Testing VoiceProcessor in Streamlit environment...")
        vp = VoiceProcessor(model_name="tiny")
        test_audio_path = input()  # Replace with a valid audio file
        if test_audio_path and os.path.exists(test_audio_path):
            with open(test_audio_path, "rb") as f:
                audio_data = f.read()
            result = vp.transcribe_audio(audio_data, filename=test_audio_path)
            if result:
                st.write("Transcription:", result['text'])
                st.write("Detected Language:", result['language'])
            else:
                st.write("Transcription failed.")
    else:
        print("Please run this script within a Streamlit environment for full functionality.")
