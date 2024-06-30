"""
Flask application for emotion detection.
"""
from flask import Flask, request, jsonify, render_template, send_from_directory
from EmotionDetection.emotion_detection import analyze_text

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    """
    Render the main page.
    """
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET', 'POST'])
def emotion_detector_api():
    """
    Emotion detection API endpoint.

    For POST requests, analyze the provided text and return the detected emotions.
    For GET requests, inform that POST is expected.
    """
    if request.method == 'POST':
        data = request.json
        if data and 'text' in data:
            text_to_analyze = data['text']
            result = analyze_text(text_to_analyze)
            if result is None or 'dominant_emotion' not in result:
                return jsonify({"error": "Invalid text! Please try again."}), 400
            return jsonify(result)
        return jsonify({"error": "Invalid request. 'text' parameter is required."}), 400

    return "GET request received, but POST is expected for emotion detection."

@app.route('/js/<path:path>')
def send_js(path):
    """
    Serve JavaScript files from the static directory.

    Args:
        path (str): Path to the JavaScript file.

    Returns:
        Response: The requested JavaScript file.
    """
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    