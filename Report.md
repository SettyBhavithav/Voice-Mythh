
Voice-to-Myth Searchable App Project Report
1. Team Information

Team Name: Myth Makers
Team Members:
Lead Developer: Kovuri Mithul
AI Specialist: Himavarshi
UI/UX Designer: Shetty Bhavithav
Database Engineer: Krishna Murthy 
Website Tester : Keerthi Nakka


Submission Date: July 24, 2025

2. Application Overview
The Voice-to-Myth Searchable App is a web-based application designed to preserve and share cultural stories (myths) from diverse linguistic backgrounds, with a focus on Indian languages. The Minimum Viable Product (MVP) enables users to:

Record or upload myths via audio or text input.
Automatically transcribe and translate stories into English.
Summarize and extract keywords for searchability.
Store myths in a database with associated metadata (location, region, image).
Search and browse myths using a keyword-based search engine.

The MVP emphasizes usability, support for multiple Indian languages (Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, and English), and robust audio processing with fallback mechanisms for limited system configurations.
3. AI Integration Details
The application leverages AI to enhance functionality:

Speech-to-Text: The VoiceProcessor component uses a speech recognition model to transcribe audio inputs. For the MVP, transcription supports WAV files natively, with conversion from other formats (e.g., MP3, M4A) using pydub or ffmpeg when available.
Translation: The TextProcessor employs a machine translation model to convert transcribed text from supported Indian languages to English, ensuring accessibility for a broader audience.
Summarization and Keyword Extraction: The TextProcessor uses natural language processing (NLP) to generate concise summaries and extract relevant keywords, enabling efficient search and indexing.
Search Engine: The SearchEngine component implements a keyword-based search algorithm, potentially enhanced with semantic search capabilities in future iterations, to retrieve relevant myths from the database.

AI models are lightweight for the MVP, prioritizing speed and compatibility with Streamlit's web-based environment. Fallback mechanisms (e.g., manual text input) ensure functionality when AI dependencies are unavailable.
4. Technical Architecture & Development
Architecture

Frontend: Streamlit provides a responsive, tab-based interface with three main sections: "Add New Myth," "Search Myths," and "All Myths." Custom CSS enhances the UI with gradients, success/warning boxes, and a sidebar for system information.
Backend Components:
VoiceProcessor: Handles audio transcription, supporting WAV files natively and other formats via conversion.
TextProcessor: Manages translation, summarization, and keyword extraction.
MythDatabase: Stores myth data (original text, English translation, summary, keywords, language, place, region, image path) using a lightweight database (e.g., SQLite for the MVP).
SearchEngine: Performs keyword-based searches on stored myths.


Dependencies:
Core: streamlit, pydub (optional), ffmpeg (optional), PIL for image handling.
File Management: os, shutil, tempfile for temporary file handling.
Audio Conversion: Fallback to ffmpeg if pydub is unavailable.


Development Process

Timeline: Developed over two weeks, with Week 1 focused on component setup (database, AI models, UI) and Week 2 on integration, testing, and refinement.
Tools: Python 3.9+, Streamlit for the frontend, and Pyodide-compatible libraries for browser-based execution.
Challenges:
Ensuring audio format compatibility with limited dependencies (e.g., no pydub or ffmpeg).
Balancing AI model performance with lightweight deployment for the MVP.
Handling temporary file cleanup to prevent storage issues.



File Structure
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


Data Collection: Feedback collected via a Google Form and direct observation of user interactions.

Findings

Successes:
90% of users successfully uploaded and processed audio/text myths.
Translation accuracy was rated 8/10 for supported languages.
Search functionality was intuitive, with 85% of users finding relevant myths within 10 seconds.
UI was praised for clarity and responsiveness.


Issues:
Users without pydub/ffmpeg faced limitations with non-WAV audio files (40% of non-technical users).
Some translations (e.g., Odia) had minor errors due to limited training data.
Image upload failed for files >5MB due to Streamlit limitations.


Feedback:
Users requested support for more audio formats without external dependencies.
Non-technical users suggested clearer instructions for installing ffmpeg.
Suggestions for adding filters (e.g., by language or region) in the search tab.


Action Plan:
Enhance error messages for audio processing failures.
Explore browser-native audio conversion to reduce dependency on ffmpeg.
Implement file size validation for image uploads.
Plan for advanced search filters in future iterations.



6. Project Lifecycle & Roadmap
A. Week 1: Rapid Development Sprint

Plan:
Set up Streamlit app structure with a tab-based UI for core functionalities.
Implement backend components: VoiceProcessor for audio transcription, TextProcessor for translation and NLP tasks, MythDatabase for storage, and SearchEngine for keyword-based search.
Integrate lightweight AI models for speech-to-text, translation, summarization, and keyword extraction.
Deploy the MVP on Hugging Face Spaces, incorporating offline-first caching using Streamlit's @st.cache_resource for low-bandwidth compatibility.


Execution:
Developed Streamlit app with three tabs ("Add New Myth," "Search Myths," "All Myths") and custom CSS for enhanced UI.
Implemented VoiceProcessor with native WAV support and fallback conversion using ffmpeg or pydub.
Set up MythDatabase using SQLite for lightweight storage of myth data.
Deployed functional MVP on Hugging Face Spaces by Day 7, supporting audio/text input, transcription, translation, summarization, keyword extraction, and search.


Key Deliverables:
Functional MVP deployed on Hugging Face Spaces with core features: audio/text input, transcription, translation, summarization, keyword extraction, database storage, and search.
Offline-first design with cached resources for low-bandwidth environments.
Initial documentation in README.md outlining setup and usage.



B. Week 2: Beta Testing & Iteration Cycle

Methodology:
Recruitment: Recruited 10 testers (5 tech-savvy from university tech clubs, 5 non-technical from storytelling communities in India) via email and WhatsApp outreach.
Tasks:
Upload and process a WAV audio file containing a Hindi myth.
Manually input a Tamil myth and verify translation/summarization.
Search myths using keywords (e.g., "Ram," "Ganga").
Browse all myths and view associated images.
Test performance on simulated low-bandwidth connections (2G/3G networks).


Feedback Collection: Used Google Forms for structured feedback (rating usability, performance, and errors) and direct observation during virtual testing sessions to capture qualitative insights, with specific questions about low-bandwidth performance.


Insights & Iterations:
Feedback:
Users found the UI intuitive but struggled with non-WAV audio uploads without pydub/ffmpeg (40% of non-technical users).
Translation accuracy rated 8/10, with minor errors in Odia and Punjabi.
Image loading was slow on 2G networks for myths with large images.
Non-technical users requested clearer instructions for installing dependencies.


Change Log:
Added detailed warning messages for missing pydub or ffmpeg.
Implemented file size validation for audio uploads (capped at 10MB).
Optimized image compression to reduce load times on low-bandwidth connections.
Updated UI with a help section for dependency installation.
Fixed a database query bug causing slow search performance on large datasets.


C. Weeks 3-4: User Acquisition & Corpus Growth Campaign

Target Audience & Channels:
Audience: Students and educators in Indian universities (e.g., Uttar Pradesh, Tamil Nadu, West Bengal), members of cultural storytelling groups, and rural community centers.
Justification: These groups are deeply connected to cultural preservation, have access to diverse linguistic myths, and are motivated to contribute to a digital archive of stories.
Channels:
WhatsApp groups for university cultural clubs and storytelling communities.
Social media platforms (Twitter/X, Instagram) targeting Indian folklore enthusiasts.
Partnerships with local NGOs focused on cultural heritage preservation.




Growth Strategy & Messaging:
Key Message: "Preserve your cultural stories with Voice-to-Myth! Record, translate, and share myths in your language to keep our heritage alive."
Promotion:
Social media campaign with demo videos showcasing audio upload, transcription, and search features.
Direct outreach to 5 university cultural clubs via WhatsApp and email.
Collaborated with 2 NGOs in Uttar Pradesh for in-person and virtual storytelling workshops.


Promotional Materials:
Twitter/X Post: "🏛️ Share your community's myths with Voice-to-Myth! Record in your language, and we'll translate and preserve it. Join the movement: [Hugging Face URL] #IndianCulture #Storytelling"
WhatsApp Flyer: A digital poster with app screenshots, a QR code linking to the app, and a call-to-action: "Record your myths today!"
Instagram Story: A 15-second video demo of uploading a myth and searching the corpus.




Execution & Results:
Actions:
Posted 10 promotional tweets and 5 Instagram stories over two weeks, reaching 2,000+ impressions.
Sent 50 targeted messages to WhatsApp groups and university contacts, engaging 200+ potential users.
Conducted 3 virtual workshops with NGOs, training 50 participants (30 rural, 20 urban) to use the app.
Monitored user activity via Hugging Face Spaces analytics and a custom tracking script for contributions.


Metrics:
Unique Users: 120 unique users acquired (80 via social media, 30 via NGO workshops, 10 via direct outreach).
Corpus Units: 85 myths contributed (50 audio, 35 text; 60% Hindi, 20% Tamil, 15% Bengali, 5% others).
User Feedback:
80% rated the app as "easy to use" via post-workshop surveys.
Positive feedback: Seamless audio transcription and intuitive search.
Issues: Limited audio format support (non-WAV files) and occasional translation errors in less common languages.
Suggestions: Add offline mode for rural users, support more languages, and include a progress bar for audio processing.

D. Post-Internship Vision & Sustainability Plan

Major Future Features:
Offline mode for audio processing and myth storage using WebAssembly to support rural users with limited connectivity.
Advanced search filters by language, region, and keyword for better corpus navigation.
Support for additional Indian languages (e.g., Assamese, Bhojpuri) to expand inclusivity.
Integration with larger language models for improved translation and summarization accuracy.


Community Building:
Launch a "Myth Makers Community" on Discord to foster user engagement, share stories, and collect feature requests.
Partner with additional NGOs and schools to host storytelling events and workshops.
Introduce a leaderboard for top contributors to encourage consistent participation.


Scaling Data Collection:
Develop a mobile app version to improve accessibility in rural areas with limited browser access.
Incentivize contributions with digital badges and recognition for high-quality myths.
Collaborate with linguistic research institutions to validate and expand the corpus.


Sustainability:
Open-source the project on GitHub to attract volunteer developers and reduce maintenance costs.
Seek grants from cultural preservation organizations (e.g., INTACH) to fund server and hosting costs.
Explore a freemium model with premium features (e.g., advanced analytics, priority support) to generate revenue for long-term maintenance.


