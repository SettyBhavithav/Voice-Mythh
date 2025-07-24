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
import io
import subprocess

# Audio processing fallback imports
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    st.warning("⚠️ pydub is not available. Some audio formats may not be supported.")

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
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        color: #856404;
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

def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            return True, ffmpeg_path
        return False, None
    except Exception:
        return False, None

def convert_audio_to_wav(input_path, output_path):
    """Convert audio to WAV format using ffmpeg"""
    try:
        if PYDUB_AVAILABLE:
            # Use pydub if available
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format='wav')
            return True
        else:
            # Use ffmpeg directly
            ffmpeg_available, ffmpeg_path = check_ffmpeg()
            if ffmpeg_available:
                result = subprocess.run([
                    'ffmpeg', '-i', input_path, '-acodec', 'pcm_s16le', 
                    '-ar', '16000', '-ac', '1', '-y', output_path
                ], capture_output=True, text=True)
                return result.returncode == 0
            return False
    except Exception as e:
        st.error(f"Error converting audio: {e}")
        return False

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

# System status check
col1, col2, col3 = st.columns(3)
with col1:
    if PYDUB_AVAILABLE:
        st.success("✅ Audio Processing: Available")
    else:
        st.warning("⚠️ Audio Processing: Limited")
with col2:
    ffmpeg_available, ffmpeg_path = check_ffmpeg()
    if ffmpeg_available:
        st.success("✅ FFmpeg: Available")
    else:
        st.warning("⚠️ FFmpeg: Not Found")
with col3:
    st.info("ℹ️ For best results, install: pip install pydub")

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
        
        # Show supported formats based on available tools
        if PYDUB_AVAILABLE and ffmpeg_available:
            supported_formats = ['wav', 'mp3', 'm4a', 'flac', 'ogg']
            format_info = "All formats supported"
        elif ffmpeg_available:
            supported_formats = ['wav', 'mp3', 'm4a']
            format_info = "Limited formats (install pydub for more)"
        else:
            supported_formats = ['wav']
            format_info = "WAV only (install ffmpeg and pydub for more formats)"
        
        st.info(f"📋 {format_info}")
        audio_file = st.file_uploader("Upload audio file:", type=supported_formats)
        
        if audio_file is not None:
            st.audio(audio_file)
            if st.button("📁 Process Audio", type="primary"):
                with st.spinner("Processing audio..."):
                    temp_file_path = None
                    wav_path = None
                    try:
                        # Read audio file as bytes
                        audio_data = audio_file.read()
                        if not audio_data:
                            st.error("❌ Uploaded audio file is empty")
                            st.stop()
                        
                        # Save uploaded audio to a temporary file
                        file_extension = audio_file.name.split('.')[-1].lower()
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
                            temp_file.write(audio_data)
                            temp_file_path = temp_file.name
                        
                        # Verify temporary file exists
                        if not os.path.exists(temp_file_path):
                            st.error(f"❌ Failed to create temporary file")
                            st.stop()
                        
                        st.info(f"📊 Processing {file_extension.upper()} file ({len(audio_data)} bytes)")
                        
                        # Convert to WAV if necessary
                        if file_extension == 'wav':
                            wav_path = temp_file_path
                            st.success("✅ WAV file detected, no conversion needed")
                        else:
                            # Need conversion
                            wav_path = os.path.join(tempfile.gettempdir(), 
                                                  f"converted_{os.path.splitext(os.path.basename(temp_file_path))[0]}.wav")
                            
                            if not PYDUB_AVAILABLE and not ffmpeg_available:
                                st.error("❌ Cannot convert audio format. Please upload WAV files or install ffmpeg/pydub.")
                                st.markdown("""
                                <div class="warning-box">
                                    <h4>🔧 Installation Instructions:</h4>
                                    <p><strong>For pydub:</strong> pip install pydub</p>
                                    <p><strong>For ffmpeg:</strong> Visit <a href="https://ffmpeg.org/download.html">ffmpeg.org</a></p>
                                </div>
                                """, unsafe_allow_html=True)
                                st.stop()
                            
                            success = convert_audio_to_wav(temp_file_path, wav_path)
                            if not success:
                                st.error("❌ Failed to convert audio format")
                                st.info("💡 Try uploading a WAV file instead")
                                st.stop()
                            else:
                                st.success(f"✅ Converted {file_extension.upper()} to WAV")
                        
                        # Verify WAV file exists
                        if not os.path.exists(wav_path):
                            st.error("❌ WAV file not found after processing")
                            st.stop()
                        
                        # Read WAV file as bytes for transcription
                        with open(wav_path, 'rb') as f:
                            wav_data = f.read()
                        
                        st.info(f"📊 Processing WAV data ({len(wav_data)} bytes)")
                        
                        # Process the audio data
                        transcription = components['voice_processor'].transcribe_audio(wav_data, audio_file.name)
                        
                        if transcription:
                            st.session_state.transcription = transcription
                            st.session_state.audio_processed = True
                            st.success("✅ Audio processed successfully!")
                        else:
                            st.error("❌ Failed to transcribe audio")
                            st.info("💡 Check if the audio contains clear speech")
                            
                    except Exception as e:
                        st.error(f"❌ Error processing audio: {str(e)}")
                        st.info("💡 Try using a different audio file or check the format")
                    finally:
                        # Clean up temporary files
                        for path in [temp_file_path, wav_path]:
                            if path and os.path.exists(path) and path != temp_file_path:
                                try:
                                    os.unlink(path)
                                except Exception as e:
                                    st.warning(f"⚠️ Could not clean up temporary file: {str(e)}")
        
        # Option 2: Manual text input
        st.write("**Type Manually**")
        manual_text = st.text_area("Enter myth text:", height=150, placeholder="Type your myth story here...", key="manual_input")
        manual_language = st.selectbox("Select Language:", 
                                     ["hi", "ta", "te", "bn", "mr", "gu", "kn", "ml", "pa", "or", "en"],
                                     format_func=lambda x: {
                                         'hi': 'Hindi', 'ta': 'Tamil', 'te': 'Telugu', 'bn': 'Bengali',
                                         'mr': 'Marathi', 'gu': 'Gujarati', 'kn': 'Kannada', 'ml': 'Malayalam',
                                         'pa': 'Punjabi', 'or': 'Odia', 'en': 'English'
                                     }.get(x, x))
        
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
                try:
                    english_text = components['text_processor'].translate_to_english(
                        transcription['text'], transcription['language']
                    )
                    summary = components['text_processor'].create_summary(english_text)
                    keywords = components['text_processor'].extract_keywords(english_text)
                except Exception as e:
                    st.error(f"Error processing text: {e}")
                    english_text = transcription['text']  # Fallback
                    summary = transcription['text'][:200] + "..."  # Simple summary
                    keywords = ["myth", "story"]  # Basic keywords
            
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
                    try:
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
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving myth: {e}")
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
            try:
                results = components['search_engine'].search(search_query)
            except Exception as e:
                st.error(f"Search error: {e}")
                results = []
        
        if results:
            st.success(f"📚 Found {len(results)} myth(s)!")
            for i, myth in enumerate(results):
                with st.expander(f"📖 Myth {i+1}: {myth.get('place', 'Unknown Location')}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**📍 Location:** {myth.get('place', 'N/A')} ({myth.get('region', 'N/A')})")
                        st.write(f"**🌐 Language:** {myth.get('language', 'N/A')}")
                        st.write(f"**📄 Summary:** {myth.get('summary', 'N/A')}")
                        keywords = myth.get('keywords', [])
                        if isinstance(keywords, list):
                            keywords_str = ', '.join(keywords)
                        else:
                            keywords_str = str(keywords)
                        st.write(f"**🏷️ Keywords:** {keywords_str}")
                        
                        if st.button(f"📖 Show Full Story #{i+1}", key=f"show_full_story_search_{i}"):
                            st.session_state[f"show_full_story_search_{i}"] = not st.session_state.get(f"show_full_story_search_{i}", False)
                        
                        if st.session_state.get(f"show_full_story_search_{i}", False):
                            st.write("**Original Text:**")
                            st.write(myth.get('original_text', 'N/A'))
                            st.write("**English Translation:**")
                            st.write(myth.get('english_text', 'N/A'))
                    with col2:
                        image_path = myth.get('image_path', '')
                        if image_path and os.path.exists(image_path):
                            try:
                                image = Image.open(image_path)
                                st.image(image, caption="Associated Image", use_column_width=True)
                            except Exception as e:
                                st.warning(f"Could not load image: {e}")
        else:
            st.info("😔 No myths found. Try different keywords!")

# Tab 3: All Myths
with tab3:
    st.header("📚 Your Myth Collection")
    
    try:
        all_myths = components['db'].get_all_myths()
    except Exception as e:
        st.error(f"Error loading myths: {e}")
        all_myths = []
    
    if all_myths:
        st.success(f"📊 Total myths: {len(all_myths)}")
        for i, myth in enumerate(all_myths):
            with st.expander(f"📖 {myth.get('place', 'Unknown')} ({myth.get('language', 'N/A')}) #{i+1}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**📄 Summary:** {myth.get('summary', 'N/A')}")
                    keywords = myth.get('keywords', [])
                    if isinstance(keywords, list):
                        keywords_str = ', '.join(keywords)
                    else:
                        keywords_str = str(keywords)
                    st.write(f"**🏷️ Keywords:** {keywords_str}")
                    
                    if st.button(f"📖 Show Full Story #{i+1}", key=f"show_full_story_all_{i}"):
                        st.session_state[f"show_full_story_all_{i}"] = not st.session_state.get(f"show_full_story_all_{i}", False)
                    
                    if st.session_state.get(f"show_full_story_all_{i}", False):
                        st.write("**Original Text:**")
                        st.write(myth.get('original_text', 'N/A'))
                        st.write("**English Translation:**")
                        st.write(myth.get('english_text', 'N/A'))
                with col2:
                    image_path = myth.get('image_path', '')
                    if image_path and os.path.exists(image_path):
                        try:
                            image = Image.open(image_path)
                            st.image(image, caption="Story Image", use_column_width=True)
                        except Exception as e:
                            st.warning(f"Could not load image: {e}")
    else:
        st.info("📭 No myths yet. Add some in the 'Add New Myth' tab!")

# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.write("**Voice-to-Myth App** helps preserve cultural stories with voice/text input, translation, and search.")
    
    st.markdown("### 📊 Stats")
    try:
        total_myths = len(components['db'].get_all_myths())
    except:
        total_myths = 0
    st.metric("Total Myths", total_myths)
    
    st.markdown("### 🌟 Languages")
    languages = {
        'hi': 'Hindi', 'ta': 'Tamil', 'te': 'Telugu', 'bn': 'Bengali', 'mr': 'Marathi',
        'gu': 'Gujarati', 'kn': 'Kannada', 'ml': 'Malayalam', 'pa': 'Punjabi', 'or': 'Odia', 'en': 'English'
    }
    for code, name in languages.items():
        st.write(f"• {name} ({code})")
    
    st.markdown("### 🔧 System Requirements")
    st.write("**For full audio support:**")
    st.code("pip install pydub ffmpeg-python")
    st.write("**FFmpeg installation:**")
    st.write("Visit [ffmpeg.org](https://ffmpeg.org/download.html)")
    
    if not PYDUB_AVAILABLE:
        st.warning("⚠️ Limited audio support")
    if not ffmpeg_available:
        st.warning("⚠️ FFmpeg not found")
