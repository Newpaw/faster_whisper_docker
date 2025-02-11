# transcription.py
# This module handles the transcription using faster-whisper.
# Since your machine is less than stellar, we use the 'small' model on CPU with int8 quantization.

from faster_whisper import WhisperModel

# Load the model only once – because reloading it for every transcription would be a colossal waste.
model = WhisperModel("small", device="cpu", compute_type="int8")


def transcribe_audio(file_path: str) -> dict:
    """
    Transcribe the given MP3 file using faster-whisper and return a JSON-like dictionary.
    The returned structure includes detected language and transcription segments.
    """
    # Run the transcription with a beam size of 5.
    segments, info = model.transcribe(file_path, beam_size=5)
    
    # Convert the segments generator into a list.
    segments = list(segments)
    
    # Build a nice JSON-like structure for the transcription result.
    result = {
        "language": {
            "detected": info.language,
            "probability": info.language_probability
        },
        "segments": []
    }
    
    # Process each transcription segment.
    for segment in segments:
        result["segments"].append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
    
    return result
