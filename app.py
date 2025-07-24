import streamlit as st
import os
import shutil
from voice_processor import VoiceProcessor
from text_processor import TextProcessor
from myth_database import MythDatabase
from search_engine import SearchEngine
from datetime import datetime
from PIL import Image
import tempfile
from pydub import AudioSegment
import io
import subprocess

# Page configuration
st.set_page_config(
    page_title="Voice-to-Myth App",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_components():
    try:
        os.makedirs("data/images", exist_ok=True)
        return {
            'voice_processor': VoiceProcessor(),
            'text_processor': TextProcessor(),
            'db': MythDatabase(),
            'search_engine': SearchEngine()
        }
    except Exception as e:
        st.error(f"Error initializing components: {e}")
        return None

# Initialize components
with st.spinner("🚀 Starting Voice-to-Myth App..."):
    components = init_components()

if not components:
    st.stop()

# App header
st.markdown("""
<div class="main-header">
    <h1>🏛️ Voice-to-Myth Searchable App</h1>
    <p>Preserve cultural stories • Translate languages • Search intelligently</p>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["📝 Add New Myth", "🔍 Search Myths", "📚 All Myths"])

# Tab 1: Add New Myth
with tab1:
    st.header("📝 Record a New Myth")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎤 Input Options")
        
        # Option 1: Upload audio file
        st.write("**Upload Audio File**")
        audio_file = st.file_uploader("Upload audio file:", type=['wav', 'mp3', 'm4a'])
        
        if audio_file is not None:
            st.audio(audio_file)
            if st.button("📁 Process Audio", type="primary"):
                with st.spinner("Processing audio..."):
                    temp_file_path = None
                    wav_path = None
                    try:
                        # Check ffmpeg availability
                        ffmpeg_path = shutil.which("ffmpeg")
                        if not ffmpeg_path:
                            st.error("❌ ffmpeg is not installed or not in system PATH")
                            st.info("💡 Install ffmpeg and add it to system PATH. Run 'ffmpeg -version' to verify. Download from https://ffmpeg.org/download.html")
                            try:
                                ffmpeg_version = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
                                st.write(f"📊 ffmpeg version: {ffmpeg_version.stdout.splitlines()[0]}")
                            except Exception as e:
                                st.write(f"📊 ffmpeg check failed: {str(e)}")
                            st.stop()
                        else:
                            st.write(f"📊 ffmpeg found at: {ffmpeg_path}")
                        
                        # Read audio file as bytes
                        audio_data = audio_file.read()
                        if not audio_data:
                            st.error("❌ Uploaded audio file is empty")
                            st.stop()
                        
                        # Save uploaded audio to a temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}") as temp_file:
                            temp_file.write(audio_data)
                            temp_file_path = temp_file.name
                        
                        # Verify temporary file exists
                        if not os.path.exists(temp_file_path):
                            st.error(f"❌ Failed to create temporary file at {temp_file_path}")
                            st.stop()
                        
                        # Debug: Log initial file details
                        st.write(f"📊 Created temporary file (size: {os.path.getsize(temp_file_path)} bytes) at {temp_file_path}")
                        
                        # Convert to WAV if necessary
                        wav_path = temp_file_path
                        if not temp_file_path.endswith('.wav'):
                            try:
                                audio = AudioSegment.from_file(temp_file_path)
                                wav_path = os.path.join(tempfile.gettempdir(), f"converted_{os.path.splitext(os.path.basename(temp_file_path))[0]}.wav")
                                audio.export(wav_path, format='wav')
                                audio._data = None  # Clear internal buffer
                            except Exception as e:
                                st.error(f"❌ Error converting audio to WAV: {str(e)}")
                                st.info("💡 Ensure ffmpeg is installed and added to system PATH. Run 'ffmpeg -version' to verify.")
                                raise
                        
                        # Verify WAV file exists
                        if not os.path.exists(wav_path):
                            st.error(f"❌ WAV file not found at {wav_path}")
                            raise FileNotFoundError(f"WAV file not found: {wav_path}")
                        
                        # Debug: Log WAV file details
                        st.write(f"📊 Processing audio file (size: {os.path.getsize(wav_path)} bytes) at {wav_path}")
                        
                        # Read WAV file as bytes for transcription
                        with open(wav_path, 'rb') as f:
                            wav_data = f.read()
                        
                        # Debug: Log size of WAV data
                        st.write(f"📊 WAV data size: {len(wav_data)} bytes")
                        
                        # Process the audio data
                        transcription = components['voice_processor'].transcribe_audio(wav_data, audio_file.name)
                        
                        if transcription:
                            st.session_state.transcription = transcription
                            st.session_state.audio_processed = True
                            st.success("✅ Audio processed successfully!")
                        else:
                            st.error("❌ Failed to transcribe audio")
                            raise Exception("Transcription returned None")
                    except Exception as e:
                        st.error(f"❌ Error processing audio: {str(e)}")
                        st.info("💡 Try using a different audio file or check audio format compatibility")
                    finally:
                        # Clean up temporary files
                        for path in [temp_file_path, wav_path]:
                            if path and os.path.exists(path):
                                try:
                                    os.unlink(path)
                                except PermissionError as pe:
                                    st.warning(f"⚠️ Could not delete temporary file {path}: {str(pe)}")
                                except Exception as e:
                                    st.warning(f"⚠️ Error during cleanup of {path}: {str(e)}")
        
        # Option 2: Manual text input
        st.write("**Type Manually**")
        manual_text = st.text_area("Enter myth text:", height=150, placeholder="Type your myth story here...", key="manual_input")
        manual_language = st.selectbox("Select Language:", 
                                     ["hi", "ta", "te", "bn", "mr", "gu", "kn", "ml", "pa", "or", "en"])
        
        if st.button("⌨️ Process Text", type="secondary") and manual_text:
            st.session_state.transcription = {
                'text': manual_text,
                'language': manual_language
            }
            st.session_state.audio_processed = True
            st.success("✅ Text processed successfully!")
    
    with col2:
        st.subheader("📋 Myth Processing & Details")
        
        if st.session_state.get('audio_processed', False):
            transcription = st.session_state.transcription
            
            # Display transcription
            st.write("**📝 Original Text:**")
            st.text_area("", transcription['text'], height=100, disabled=True, key="transcription_text")
            st.write(f"**🌐 Language:** {transcription['language']}")
            
            # Process text
            with st.spinner("🔄 Processing text..."):
                english_text = components['text_processor'].translate_to_english(
                    transcription['text'], transcription['language']
                )
                summary = components['text_processor'].create_summary(english_text)
                keywords = components['text_processor'].extract_keywords(english_text)
            
            # Display results
            st.write("**🌍 English Translation:**")
            st.text_area("", english_text, height=100, disabled=True, key="english_translation")
            st.write("**📄 Summary:**")
            st.text_area("", summary, height=68, disabled=True, key="summary_text")
            st.write("**🏷️ Keywords:**")
            st.write(", ".join(keywords))
            
            # Additional details
            st.write("**📍 Additional Information:**")
            col2a, col2b = st.columns(2)
            with col2a:
                place = st.text_input("Place/Location:", placeholder="e.g., Ayodhya")
            with col2b:
                region = st.text_input("Region/State:", placeholder="e.g., Uttar Pradesh")
            
            # Image upload
            uploaded_image = st.file_uploader("📸 Upload image (optional):", type=['png', 'jpg', 'jpeg'])
            
            # Save to database
            if st.button("💾 Save Myth", type="primary"):
                with st.spinner("Saving myth..."):
                    image_path = ""
                    if uploaded_image:
                        image_path = f"data/images/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_image.name}"
                        with open(image_path, "wb") as f:
                            f.write(uploaded_image.read())
                    
                    myth_data = {
                        'original_text': transcription['text'],
                        'english_text': english_text,
                        'summary': summary,
                        'keywords': keywords,
                        'language': transcription['language'],
                        'place': place,
                        'region': region,
                        'image_path': image_path
                    }
                    
                    myth_id = components['db'].insert_myth(myth_data)
                    st.markdown(f"""
                    <div class="success-box">
                        <h4>✅ Myth Saved Successfully!</h4>
                        <p><strong>ID:</strong> {myth_id}</p>
                        <p><strong>Location:</strong> {place}, {region}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.audio_processed = False
                    st.session_state.transcription = None
        else:
            st.info("👆 Choose an input method to start!")

# Tab 2: Search Myths
with tab2:
    st.header("🔍 Search Your Myth Collection")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔎 Search myths:", placeholder="e.g., Ram, Krishna, Ganga")
    with col2:
        search_button = st.button("🔍 Search", type="primary")
    
    if search_query and (search_button or search_query):
        with st.spinner("🔍 Searching..."):
            results = components['search_engine'].search(search_query)
        
        if results:
            st.success(f"📚 Found {len(results)} myth(s)!")
            for i, myth in enumerate(results):
                with st.expander(f"📖 Myth {i+1}: {myth['place']}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**📍 Location:** {myth['place']} ({myth['region']})")
                        st.write(f"**🌐 Language:** {myth['language']}")
                        st.write(f"**📄 Summary:** {myth['summary']}")
                        st.write(f"**🏷️ Keywords:** {', '.join(myth['keywords'])}")
                        if st.button(f"📖 Show Full Story #{i+1}", key=f"show_full_story_{i}"):
                            st.session_state[f"show_full_story_{i}"] = not st.session_state.get(f"show_full_story_{i}", False)
                        if st.session_state.get(f"show_full_story_{i}", False):
                            st.write("**Original Text:**")
                            st.write(myth['original_text'])
                            st.write("**English Translation:**")
                            st.write(myth['english_text'])
                    with col2:
                        if myth['image_path'] and os.path.exists(myth['image_path']):
                            image = Image.open(myth['image_path'])
                            st.image(image, caption="Associated Image", use_column_width=True)
        else:
            st.info("😔 No myths found. Try different keywords!")

# Tab 3: All Myths
with tab3:
    st.header("📚 Your Myth Collection")
    
    all_myths = components['db'].get_all_myths()
    
    if all_myths:
        st.success(f"📊 Total myths: {len(all_myths)}")
        for i, myth in enumerate(all_myths):
            with st.expander(f"📖 {myth['place']} ({myth['language']}) #{i+1}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**📄 Summary:** {myth['summary']}")
                    st.write(f"**🏷️ Keywords:** {', '.join(myth['keywords'])}")
                    if st.button(f"📖 Show Full Story #{i+1}", key=f"show_full_story_{i}"):
                        st.session_state[f"show_full_story_{i}"] = not st.session_state.get(f"show_full_story_{i}", False)
                    if st.session_state.get(f"show_full_story_{i}", False):
                        st.write("**Original Text:**")
                        st.write(myth['original_text'])
                        st.write("**English Translation:**")
                        st.write(myth['english_text'])
                with col2:
                    if myth['image_path'] and os.path.exists(myth['image_path']):
                        image = Image.open(myth['image_path'])
                        st.image(image, caption="Story Image", use_column_width=True)
    else:
        st.info("📭 No myths yet. Add some in the 'Add New Myth' tab!")

# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.write("**Voice-to-Myth App** helps preserve cultural stories with voice/text input, translation, and search.")
    st.markdown("### 📊 Stats")
    st.metric("Total Myths", len(components['db'].get_all_myths()))
    st.markdown("### 🌟 Languages")
    languages = {'hi': 'Hindi', 'ta': 'Tamil', 'te': 'Telugu', 'bn': 'Bengali', 'mr': 'Marathi',
                 'gu': 'Gujarati', 'kn': 'Kannada', 'ml': 'Malayalam', 'pa': 'Punjabi', 'or': 'Odia', 'en': 'English'}
    for code, name in languages.items():
        st.write(f"• {name} ({code})")
