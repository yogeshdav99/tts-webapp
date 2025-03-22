from flask import Flask, render_template, request, send_file, send_from_directory
from TTS.api import TTS
import os

app = Flask(__name__)
MODELS = {
    "English (Default)": "tts_models/en/ljspeech/tacotron2-DDC",
    "Spanish": "tts_models/es/css10/vits"    
}


# Create audio directory if not exists
if not os.path.exists("audio"):
    os.makedirs("audio")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get form data
        text = request.form['text'].replace('—', '-')
        voice = request.form.get('voice', 'English (Default)')
        
        # Validate input
        if not text:
            raise ValueError("Please enter some text")
        if len(text) > 1000:
            raise ValueError("Text exceeds 1000 character limit")
            
        # Initialize TTS with selected voice
        model_name = MODELS.get(voice, MODELS["English (Default)"])
        tts = TTS(model_name=model_name, gpu=False)
        
        # Generate audio
        output_path = "audio/output.wav"
        tts.tts_to_file(text=text, file_path=output_path)
        
        return render_template('index.html', 
                            audio_available=True,
                            success="Audio generated successfully!")
        
    except Exception as e:
        return render_template('index.html', 
                             error=str(e),
                             audio_available=False)

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory("audio", filename)

if __name__ == '__main__':
    app.run(debug=True)
