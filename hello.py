from faster_whisper import WhisperModel

def transcribe_audio(file_path: str) -> None:
    """
    Transcribes the audio file at the given file_path using faster-whisper.
    This function prints out the detected language and transcription segments.
    """
    # Step 1: Initialize the model
    # Use a small model for Raspberry Pi 3B+; adjust the model size if needed
    model_size = "small"
    # Initialize the WhisperModel on CPU with INT8 quantization to reduce resource usage
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
    # Step 2: Notify the start of transcription
    print(f"Starting transcription for file: {file_path}")
    
    # Step 3: Transcribe the audio file with a beam size of 5
    segments, info = model.transcribe(file_path, beam_size=5)
    
    # Step 4: Print detected language and its probability
    print("Detected language: {} with probability: {:.2f}".format(info.language, info.language_probability))
    
    # Step 5: Iterate over each segment and print its start time, end time, and text
    for segment in segments:
        print("[{:.2f}s -> {:.2f}s]: {}".format(segment.start, segment.end, segment.text))

if __name__ == "__main__":
    # Example usage: call the function with the path to your MP3 file.
    # Replace 'audio.mp3' with the actual path to your audio file.
    transcribe_audio("audio.mp3")

