from flask import Flask, jsonify, render_template, request, send_from_directory
from TTS.api import TTS
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

MODELS = {
    "English (Default)": "tts_models/en/ljspeech/tacotron2-DDC",
    "Spanish": "tts_models/es/css10/vits"    
}

if not os.path.exists("audio"):
    os.makedirs("audio")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        text = request.form['text'].strip().replace('—', '-')
        voice = request.form.get('voice', 'English (Default)')

        if not text:
            return jsonify({"error": "Please enter some text"}), 400
        if len(text) > 1000:
            return jsonify({"error": "Text exceeds 1000 character limit"}), 400

        model_name = MODELS.get(voice)
        if not model_name:
            return jsonify({"error": "Invalid voice selection"}), 400

        filename = f"output_{uuid.uuid4().hex}.wav"
        output_path = os.path.join("audio", filename)

        tts = TTS(model_name=model_name, gpu=False)
        tts.tts_to_file(text=text, file_path=output_path)
        
        return jsonify({
            "success": "Audio generated successfully!",
            "audio_url": f"/audio/{filename}"
        })
        
    except Exception as e:
        app.logger.error(f"Generation error: {str(e)}")
        return jsonify({"error": f"Audio generation failed: {str(e)}"}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory("audio", secure_filename(filename))

if __name__ == '__main__':
    app.run(debug=True)