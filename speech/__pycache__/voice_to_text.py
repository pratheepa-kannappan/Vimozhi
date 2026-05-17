from speech.wish import model

def voice_to_text(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]