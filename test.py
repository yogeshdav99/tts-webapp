from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=False)
tts.tts_to_file(text="Hello! Teri ma ki chut bhosdike.", file_path="test.wav")
print("Done! Check test.wav in your folder!")