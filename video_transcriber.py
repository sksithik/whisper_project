import os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import whisper


def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    print(f"Audio extracted to {audio_path}")
 
    
def transcribe_audio(audio_path):

    model = whisper.load_model("base")
    
    # Transcribe the audio file
    result = model.transcribe(audio_path)
    return result["text"]
    # Print the transcription

    
def add_text_to_video(video_path, output_path, text):
    video = VideoFileClip(video_path)
    text_clip = TextClip(text, fontsize=24, color='white', bg_color='black', size=(video.w, None))
    text_clip = text_clip.set_duration(video.duration).set_position(("center", "bottom"))
    
    final_video = CompositeVideoClip([video, text_clip])
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Video with transcript saved to {output_path}")

def main():
    video_path = input("Enter the path to the video file: ").strip()
    if not os.path.exists(video_path):
        print("Video file not found!")
        return
    
    audio_path = "temp_audio.wav"
    output_path = "output_video.mp4"
    
    # Step 1: Extract audio from video
    extract_audio_from_video(video_path, audio_path)
    
    # Step 2: Transcribe audio
    transcript = transcribe_audio(audio_path)
    print("Transcript:", transcript)
    
    # Step 3: Add transcript to video
    add_text_to_video(video_path, output_path, transcript)
    
    # Clean up
    os.remove(audio_path)
    print("Temporary files cleaned up.")

if __name__ == "__main__":
    main()