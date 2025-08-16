# Overview

HablaPRO is a comprehensive presentation skills analysis application built with Streamlit that provides AI-powered feedback on various aspects of public speaking. The system analyzes uploaded videos to evaluate voice quality, body language, and facial expressions, offering detailed scoring and actionable feedback to help users improve their presentation abilities. The application is designed primarily for educational environments, allowing students to submit presentation videos and receive detailed analysis reports.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Streamlit Framework**: Web-based interface using Streamlit for rapid development and deployment
- **Multi-column Layout**: Organized user interface with sidebar for user information and main content area for video upload and analysis results
- **Interactive Visualization**: Real-time chart generation and display using matplotlib and seaborn for score visualization
- **Session State Management**: Streamlit's caching system for component initialization and data persistence

## Backend Architecture
- **Modular Analysis System**: Separate analyzer classes for different aspects (voice, body language, facial expressions)
- **Media Processing Pipeline**: Video processing workflow that extracts audio and analyzes visual components sequentially
- **Data Storage Layer**: JSON-based file storage system organized by student profiles and analysis sessions
- **Chart Generation Service**: Dedicated visualization component for creating analysis reports and progress tracking

## AI/ML Components
- **Voice Analysis**: Whisper model integration for speech transcription and audio feature extraction using librosa
- **Computer Vision**: MediaPipe integration for pose detection, facial landmark detection, and gesture recognition
- **Audio Processing**: Librosa for advanced audio feature analysis including pitch, tempo, and prosody detection
- **Real-time Processing**: Frame-by-frame analysis with optimization for performance (processing every 5th frame)

## Data Processing
- **Video Input Handling**: Support for multiple video formats (MP4, AVI, MOV, MKV) with validation and preprocessing
- **Audio Extraction**: Temporary audio file creation from video for separate voice analysis
- **Feature Extraction**: Multi-modal feature extraction from audio, visual, and textual components
- **Score Calculation**: Weighted scoring system combining multiple analysis metrics into overall performance scores

## Storage Architecture
- **File-based Storage**: Local JSON file storage organized in hierarchical directory structure
- **Student Profiles**: Individual student directories with historical analysis data
- **Analysis Archives**: Timestamped analysis results with metadata for tracking progress over time
- **Data Serialization**: JSON format for cross-platform compatibility and human-readable storage

# External Dependencies

## AI/ML Libraries
- **OpenAI Whisper**: Speech recognition and transcription for voice analysis
- **MediaPipe**: Google's framework for pose detection, facial landmark detection, and gesture recognition
- **librosa**: Advanced audio analysis library for prosody and speech feature extraction

## Computer Vision
- **OpenCV**: Video processing, frame extraction, and basic image operations
- **NumPy**: Numerical computing for array operations and mathematical calculations

## Data Visualization
- **matplotlib**: Primary plotting library for chart generation and data visualization
- **seaborn**: Statistical data visualization built on matplotlib for enhanced styling
- **pandas**: Data manipulation and analysis for handling analysis results

## Web Framework
- **Streamlit**: Web application framework for rapid deployment and interactive interfaces

## File Processing
- **tempfile**: Temporary file management for audio extraction and processing
- **pathlib**: Modern path handling and file system operations
- **json**: Data serialization and storage format for analysis results

## Audio/Video Processing
- **cv2 (OpenCV)**: Video file handling, frame extraction, and basic video properties analysis
- **ffmpeg** (implicit): Video format support and audio extraction capabilities through librosa and OpenCV