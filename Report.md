
#Voice-to-Myth Searchable App Project Report
##1. Team Information

Team Name: Myth Makers
Team Members:
Lead Developer: Kovuri Mithul
AI Specialist: Himavarshi
UI/UX Designer: Shetty Bhavithav
Database Engineer: Krishna Murthy 
Website Tester : Keerthi Nakka


Submission Date: July 24, 2025

##2. Application Overview
The Voice-to-Myth Searchable App is a web-based application designed to preserve and share cultural stories (myths) from diverse linguistic backgrounds, with a focus on Indian languages. The Minimum Viable Product (MVP) enables users to:

Record or upload myths via audio or text input.
Automatically transcribe and translate stories into English.
Summarize and extract keywords for searchability.
Store myths in a database with associated metadata (location, region, image).
Search and browse myths using a keyword-based search engine.

The MVP emphasizes usability, support for multiple Indian languages (Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, and English), and robust audio processing with fallback mechanisms for limited system configurations.
##3. AI Integration Details
The application leverages AI to enhance functionality:

Speech-to-Text: The VoiceProcessor component uses a speech recognition model to transcribe audio inputs. For the MVP, transcription supports WAV files natively, with conversion from other formats (e.g., MP3, M4A) using pydub or ffmpeg when available.
Translation: The TextProcessor employs a machine translation model to convert transcribed text from supported Indian languages to English, ensuring accessibility for a broader audience.
Summarization and Keyword Extraction: The TextProcessor uses natural language processing (NLP) to generate concise summaries and extract relevant keywords, enabling efficient search and indexing.
Search Engine: The SearchEngine component implements a keyword-based search algorithm, potentially enhanced with semantic search capabilities in future iterations, to retrieve relevant myths from the database.

AI models are lightweight for the MVP, prioritizing speed and compatibility with Streamlit's web-based environment. Fallback mechanisms (e.g., manual text input) ensure functionality when AI dependencies are unavailable.
##4. Technical Architecture & Development
Architecture

Frontend: Streamlit provides a responsive, tab-based interface with three main sections: "Add New Myth," "Search Myths," and "All Myths." Custom CSS enhances the UI with gradients, success/warning boxes, and a sidebar for system information.
Backend Components:
VoiceProcessor: Handles audio transcription, supporting WAV files natively and other formats via conversion.
TextProcessor: Manages translation, summarization, and keyword extraction.
MythDatabase: Stores myth data (original text, English translation, summary, keywords, language, place, region, image path) using a lightweight database (e.g., SQLite for the MVP).
SearchEngine: Performs keyword-based searches on stored myths.


###Dependencies:
Core: streamlit, pydub (optional), ffmpeg (optional), PIL for image handling.
File Management: os, shutil, tempfile for temporary file handling.
Audio Conversion: Fallback to ffmpeg if pydub is unavailable.



###Development Process

Timeline: Developed over two weeks, with Week 1 focused on component setup (database, AI models, UI) and Week 2 on integration, testing, and refinement.
Tools: Python 3.9+, Streamlit for the frontend, and Pyodide-compatible libraries for browser-based execution.
Challenges:
Ensuring audio format compatibility with limited dependencies (e.g., no pydub or ffmpeg).
Balancing AI model performance with lightweight deployment for the MVP.
Handling temporary file cleanup to prevent storage issues.



##File Structure
voice-to-myth-app/
├── data/
│   └── images/               # Stores uploaded images
├── voice_processor.py       # Audio transcription logic
├── text_processor.py        # Text translation, summarization, keyword extraction
├── myth_database.py         # Database operations
├── search_engine.py         # Search functionality
├── main.py                  # Main Streamlit app
└── REPORT.md                # Project report

##5. User Testing & Feedback
Methodology
User testing was conducted in Week 2 with a focus on the MVP's core features:

Participants: 10 users (5 tech-savvy, 5 non-technical) familiar with Indian cultural stories.
Testing Environment: Browser-based testing on Chrome and Firefox, with and without pydub/ffmpeg installed.
Test Cases:
Upload and process a WAV audio file containing a myth in Hindi.
Manually input a Tamil myth and verify translation/summarization.
Search for myths using keywords (e.g., "Ram," "Ganga").
Browse all myths and view associated images.
Test fallback mechanisms (e.g., manual text input when audio processing fails).


###Data Collection: Feedback collected via a Google Form and direct observation of user interactions.

###Findings

###Successes:
90% of users successfully uploaded and processed audio/text myths.
Translation accuracy was rated 8/10 for supported languages.
Search functionality was intuitive, with 85% of users finding relevant myths within 10 seconds.
UI was praised for clarity and responsiveness.


###Issues:
Users without pydub/ffmpeg faced limitations with non-WAV audio files (40% of non-technical users).
Some translations (e.g., Odia) had minor errors due to limited training data.
Image upload failed for files >5MB due to Streamlit limitations.


###Feedback:
Users requested support for more audio formats without external dependencies.
Non-technical users suggested clearer instructions for installing ffmpeg.
Suggestions for adding filters (e.g., by language or region) in the search tab.


###Action Plan:
Enhance error messages for audio processing failures.
Explore browser-native audio conversion to reduce dependency on ffmpeg.
Implement file size validation for image uploads.
Plan for advanced search filters in future iterations.


