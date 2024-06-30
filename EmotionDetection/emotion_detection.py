# emotion_detection.py
import requests
import json

def emotion_detector(text_to_analyze):
    if not text_to_analyze:
        return {"emotionPredictions": [{"emotion": {"anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None}}]}
    
    URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    try:
        response = requests.post(URL, json=input_json, headers=headers)
        if response.status_code == 400:
            return {"emotionPredictions": [{"emotion": {"anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None}}]}
        response.raise_for_status()
        formatted_response = json.loads(response.text)
        return formatted_response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching emotion data: {e}")
        return {"emotionPredictions": [{"emotion": {"anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None}}]}

def emotion_predictor(detected_text):
    try:
        emotions = detected_text['emotionPredictions'][0]['emotion']
        # Check if all values are None
        if all(value is None for value in emotions.values()):
            return None
        max_emotion = max(emotions, key=emotions.get)
        formatted_dict_emotions = {
            'anger': emotions['anger'],
            'disgust': emotions['disgust'],
            'fear': emotions['fear'],
            'joy': emotions['joy'],
            'sadness': emotions['sadness'],
            'dominant_emotion': max_emotion,
            'dominant_emotion_statement': f"The dominant emotion is {max_emotion.capitalize()}."
        }
        return formatted_dict_emotions
    except (KeyError, IndexError) as e:
        print(f"Error processing emotion data: {e}")
        return None

def analyze_text(text):
    detected_text = emotion_detector(text)
    if detected_text is not None:
        return emotion_predictor(detected_text)
    else:
        return {"error": "Failed to detect emotions."}
