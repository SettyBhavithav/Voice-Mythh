# Voice-Mythh

# Voice-to-Myth Searchable App
Overview
The Voice-to-Myth App is a Streamlit-based web application designed to preserve cultural stories through voice recordings or text input. It supports multiple audio formats, transcribes audio, translates text to English, generates summaries, extracts keywords, and stores myths in a searchable database. Users can upload audio or text, add metadata like location, and search their collection with advanced filters.
Features

### Audio Processing: Supports multiple audio formats (WAV, MP3, M4A, FLAC, OGG, AAC) with conversion to WAV for processing.
Transcription: Converts audio to text using a voice processor (requires implementation of VoiceProcessor).
Translation & Processing: Translates non-English text to English, generates summaries, and extracts keywords (requires TextProcessor).
Database Storage: Stores myths with metadata (location, region, image) in a database (requires MythDatabase).
Search Functionality: Intelligent search with filters for language, region, and place (requires SearchEngine).
User Interface: Streamlit-based UI with tabs for adding myths, searching, and viewing collections in grid or list view.
Image Support: Optional image uploads for myths, stored in data/images.
Maintenance Mode: Environment-based maintenance mode support.
Cleanup: Automatic cleanup of temporary files.

### Prerequisites

Python: 3.8 or higher
Dependencies:
streamlit
librosa (recommended for full audio format support)
soundfile
scipy (fallback for WAV processing)
mutagen (for audio metadata)
Pillow (for image handling)


FFmpeg: Required for audio conversion if librosa is unavailable.
Custom Modules:
voice_processor.py (for audio transcription)
text_processor.py (for translation, summarization, and keyword extraction)
myth_database.py (for database operations)
search_engine.py (for search functionality)



### Installation

Clone the Repository:
git clone <repository-url>
cd voice-to-myth-app


Set Up a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


### Install Dependencies:
pip install streamlit librosa soundfile scipy mutagen Pillow


Install FFmpeg:

On Ubuntu/Debian:sudo apt-get install ffmpeg


On macOS:brew install ffmpeg


On Windows: Download from FFmpeg website and add to PATH.


Set Up Folder Structure:
mkdir -p data/images


Implement Custom Modules:Ensure the following modules are implemented and placed in the project directory:

VoiceProcessor: Handles audio transcription.
TextProcessor: Manages translation, summarization, and keyword extraction.
MythDatabase: Manages database operations (e.g., SQLite, MongoDB).
SearchEngine: Implements search logic.



Usage

Run the Application:
streamlit run app.py

Replace app.py with the name of your main script file.

Access the App:Open a web browser and navigate to http://localhost:8501 (default Streamlit port).

Features Overview:

Add New Myth: Upload an audio file (WAV, MP3, etc.) or enter text manually. Specify language and location details. Optionally upload an image.
Search Myths: Search the collection using keywords, with filters for language, region, or place.
All Myths: View all stored myths in grid or list view, with details like summary, keywords, and images.



Configuration

Environment Variables:

MAINTENANCE_MODE: Set to true to enable maintenance mode (default: False).
Example:export MAINTENANCE_MODE=true




### Supported Languages:

Hindi (hi), Tamil (ta), Telugu (te), Bengali (bn), Marathi (mr), Gujarati (gu), Kannada (kn), Malayalam (ml), Punjabi (pa), Odia (or), English (en).


File Storage:

Images are stored in data/images/.
Temporary audio files are cleaned up automatically.



### Development Notes

Custom Modules: The app relies on four unimplemented modules (VoiceProcessor, TextProcessor, MythDatabase, SearchEngine). You must provide implementations for these to enable full functionality.
Audio Processing:
librosa is preferred for audio conversion.
FFmpeg is used as a fallback.
scipy supports WAV files only.


Error Handling: Comprehensive error handling is included for audio processing, database operations, and search.
UI: Custom CSS and smooth scrolling enhance the user experience.

Troubleshooting

Audio Conversion Fails:
Ensure FFmpeg is installed and accessible in PATH.
Install librosa and soundfile for better format support:pip install librosa soundfile




No Transcription:
Verify VoiceProcessor implementation.
Check audio quality and clarity.


Database Errors:
Ensure MythDatabase is properly configured (e.g., correct database connection).


Images Not Displaying:
Verify data/images exists and is writable.
Check image formats (PNG, JPG, JPEG supported).



Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit changes (git commit -m 'Add YourFeature').
Push to the branch (git push origin feature/YourFeature).
Open a pull request.

License
This project is licensed under the MIT License.
