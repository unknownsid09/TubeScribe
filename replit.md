# YouTube Transcript Extractor

## Overview

A Flask-based web application that extracts transcripts from YouTube videos. Users can input a YouTube video URL and receive the video's transcript in return. The application features a clean, dark-themed interface and handles various YouTube URL formats.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates (Flask's default)
- **UI Framework**: Bootstrap 5 with dark theme
- **Icons**: Font Awesome 6.0
- **Layout**: Single-page application with responsive design
- **Form Handling**: HTML forms with client-side validation

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Application Structure**: Simple modular approach with separate app.py and main.py
- **URL Routing**: RESTful endpoints for health checks and transcript extraction
- **Error Handling**: Custom error handling for YouTube API exceptions
- **CORS**: Enabled for cross-origin requests using Flask-CORS

### Data Processing
- **YouTube Integration**: Uses youtube-transcript-api library for transcript extraction
- **URL Parsing**: Regular expressions to handle multiple YouTube URL formats
- **Video ID Extraction**: Supports standard YouTube URLs, shortened youtu.be links, and mobile URLs

### Security Features
- **Session Management**: Flask sessions with configurable secret key
- **Environment Variables**: Uses environment variables for sensitive configuration
- **Input Validation**: URL format validation and sanitization

## External Dependencies

### Python Libraries
- **Flask**: Web framework for Python
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **youtube-transcript-api**: YouTube transcript extraction
- **Standard Library**: os, re, logging for core functionality

### Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme support
- **Font Awesome 6**: Icon library for UI elements

### Third-party Services
- **YouTube API**: Indirect usage through youtube-transcript-api for transcript retrieval
- **CDN Services**: Bootstrap and Font Awesome served from CDNs

### Runtime Environment
- **Python**: Web server runtime
- **Flask Development Server**: Local development and testing