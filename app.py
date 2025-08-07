import os
import re
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Enable CORS for all routes
CORS(app)

def extract_video_id(url):
    """
    Extract video ID from various YouTube URL formats
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://youtube.com/watch?v=VIDEO_ID
    - https://m.youtube.com/watch?v=VIDEO_ID
    """
    if not url:
        return None
    
    # Regular expressions for different YouTube URL formats
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:m\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

@app.route('/')
def index():
    """Render the main HTML interface"""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "OK"}), 200

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Extract transcript from YouTube video
    Expects JSON body with 'url' key
    Returns JSON with video_id and transcript
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Invalid request format. Expected JSON body."
            }), 400
        
        url = data.get('url')
        
        if not url:
            return jsonify({
                "error": "Missing 'url' field in request body."
            }), 400
        
        # Extract video ID from URL
        video_id = extract_video_id(url)
        
        if not video_id:
            return jsonify({
                "error": "Invalid YouTube URL format. Please provide a valid YouTube video URL."
            }), 400
        
        # Get transcript using youtube-transcript-api
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Format transcript as a single text string
            full_transcript = " ".join([entry['text'] for entry in transcript_list])
            
            return jsonify({
                "video_id": video_id,
                "transcript": full_transcript,
                "transcript_segments": transcript_list
            }), 200
            
        except TranscriptsDisabled:
            return jsonify({
                "error": "Transcripts are disabled for this video.",
                "video_id": video_id
            }), 404
            
        except NoTranscriptFound:
            return jsonify({
                "error": "No transcript found for this video. The video may not have captions available.",
                "video_id": video_id
            }), 404
            
        except VideoUnavailable:
            return jsonify({
                "error": "Video is unavailable or does not exist.",
                "video_id": video_id
            }), 404
            
        except Exception as e:
            app.logger.error(f"Unexpected error fetching transcript: {str(e)}")
            return jsonify({
                "error": f"Failed to fetch transcript: {str(e)}",
                "video_id": video_id
            }), 500
    
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
