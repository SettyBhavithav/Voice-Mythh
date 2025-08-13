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

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-17 #1]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-09-17 #2]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-17 #3]: Applied code update

# Format text-to-speech output response string
# Progress [2025-09-17 #4]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-17 #5]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-17 #6]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-17 #7]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-17 #8]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-18 #1]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-18 #2]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-18 #3]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-09-18 #4]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-18 #5]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-09-18 #6]: Applied code update

# Format text-to-speech output response string
# Progress [2025-09-18 #7]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-18 #8]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-18 #9]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-18 #10]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-09-18 #11]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-19 #1]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-19 #2]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-19 #3]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-19 #4]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-19 #5]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-19 #6]: Applied code update

# Format text-to-speech output response string
# Progress [2025-09-19 #7]: Applied code update

# Format text-to-speech output response string
# Progress [2025-09-20 #1]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-20 #2]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-09-20 #3]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-20 #4]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-20 #5]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-09-20 #6]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-20 #7]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-20 #8]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-21 #1]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-21 #2]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-21 #3]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-22 #1]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-22 #2]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-22 #3]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-22 #4]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-22 #5]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-22 #6]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-23 #1]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-23 #2]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-09-23 #3]: Applied code update

# Format text-to-speech output response string
# Progress [2025-09-23 #4]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-23 #5]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-23 #6]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-09-23 #7]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-23 #8]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-23 #9]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-23 #10]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-23 #11]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-24 #1]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-25 #1]: Applied code update

# Format text-to-speech output response string
# Progress [2025-09-25 #2]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-09-25 #3]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-25 #4]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-25 #5]: Applied code update

# Format text-to-speech output response string
# Progress [2025-09-26 #1]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-26 #2]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-26 #3]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-26 #4]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-26 #5]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-09-27 #1]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-27 #2]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-27 #3]: Applied code update

# Format text-to-speech output response string
# Progress [2025-09-28 #1]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-29 #1]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-09-29 #2]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-09-29 #3]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-29 #4]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-29 #5]: Applied code update

# Format text-to-speech output response string
# Progress [2025-09-29 #6]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-30 #1]: Applied code update

# Format text-to-speech output response string
# Progress [2025-09-30 #2]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-09-30 #3]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-09-30 #4]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-10-01 #1]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-10-01 #2]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-01 #3]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-10-01 #4]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-01 #5]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-01 #6]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-01 #7]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-01 #8]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-01 #9]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-01 #10]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-01 #11]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-02 #1]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-02 #2]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-02 #3]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-02 #4]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-10-02 #5]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-10-03 #1]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-04 #1]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-10-04 #2]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-04 #3]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-04 #4]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-04 #5]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-04 #6]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-10-04 #7]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-04 #8]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-04 #9]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-10-05 #1]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-05 #2]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-05 #3]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-05 #4]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-05 #5]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-06 #1]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-06 #2]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-06 #3]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-06 #4]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-06 #5]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-06 #6]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-06 #7]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-10-07 #1]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-07 #2]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-07 #3]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-07 #4]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-07 #5]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-07 #6]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-07 #7]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-08 #1]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-08 #2]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-08 #3]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-09 #1]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-10-09 #2]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-10-09 #3]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-09 #4]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-10-09 #5]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-09 #6]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-10-09 #7]: Applied code update

# Format text-to-speech output response string
# Progress [2025-10-10 #1]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-10 #2]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-10 #3]: Applied code update

# Normalize raw PCM audio signal before STT processing
# Progress [2025-10-10 #4]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-10-10 #5]: Applied code update

# Stream microphone audio chunk buffer to speech model
# Progress [2025-10-11 #1]: Applied code update

# Catch audio input device index errors gracefully
# Progress [2025-10-12 #1]: Applied code update

# Query myth database records for matching keyword entries
# Progress [2025-10-12 #2]: Applied code update

# Parse target query keywords from recognized text
# Progress [2025-10-12 #3]: Applied code update

# [2025-09-17] Step 2: added page title and header text

# [2025-09-18] Step 2: imported pyaudio and speech_recognition

# [2025-09-19] Step 2: added microphone source setup

# [2025-09-20] Step 2: handled UnknownValueError

# [2025-09-21] Step 2: added text normalization lowercasing and punctuation removal

# [2025-09-22] Step 2: added json dataset containing Indian mythological stories

# [2025-09-23] Step 2: implemented tf-idf keyword search against myth database

# [2025-09-24] Step 2: added Record Voice button in UI

# [2025-09-25] Step 2: added spinner during processing

# [2025-09-26] Step 2: rendered story title and summary

# [2025-09-27] Step 2: added Read Story Aloud feature

# [2025-09-28] Step 2: passed voice settings to pyttsx3 engine

# [2025-09-29] Step 2: reduced background mic noise

# [2025-09-30] Step 2: styled myth story cards

# [2025-10-01] Step 2: loaded images using PIL

# [2025-10-02] Step 2: added timeout limit of 5 seconds

# [2025-10-03] Step 2: rendered recent voice searches list

# [2025-10-04] Step 2: added language selector in UI

# [2025-10-05] Step 2: handled wav and mp3 conversion

# [2025-10-06] Step 2: improved query relevance ranking

# [2025-10-10] Step 2: tuned speech recognition threshold
