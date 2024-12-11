import whisper

def transcribe_audio(file_path):
    # Load the Whisper model
    model = whisper.load_model("base")
    
    # Transcribe the audio file
    result = model.transcribe(file_path)
    
    # Print the transcription
    print("Transcription:")
    print(result["text"])

if __name__ == "__main__":
    # Specify the path to your audio file
    audio_file = "sample-0.mp3"  # Replace with your file name
    transcribe_audio(audio_file)
