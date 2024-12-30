import os
import shlex
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from moviepy import VideoFileClip
import whisper
import subprocess

app = FastAPI()

# Helper functions
def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    print(f"Audio extracted to {audio_path}")

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

def add_text_with_ffmpeg(input_video_path, output_video_path, text, font="Arial.ttf", font_size=36, font_color="white", x=10, y=50):
    safe_text = text.replace("'", "\\'")
    command = [
        "ffmpeg",
        "-i", input_video_path,
        "-vf", f"drawtext=fontfile={shlex.quote(font)}:text='{safe_text}':x={x}:y={y}:fontsize={font_size}:fontcolor={font_color}",
        "-codec:a", "copy",
        output_video_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Video with text saved to {output_video_path}")
    except subprocess.CalledProcessError as e:
        raise Exception(f"An error occurred while processing the video: {e}")

# API route
@app.post("/process-video/")
async def process_video(file: UploadFile = File(...)):
    # Create unique paths for the files
    video_filename = f"{uuid.uuid4()}_{file.filename}"
    audio_filename = f"{uuid.uuid4()}.wav"
    output_filename = f"output_{uuid.uuid4()}.mp4"

    try:
        # Save the uploaded video file
        video_path = f"temp_{video_filename}"
        with open(video_path, "wb") as f:
            f.write(await file.read())

        # Step 1: Extract audio
        extract_audio_from_video(video_path, audio_filename)

        # Step 2: Transcribe audio
        transcript = transcribe_audio(audio_filename)
        print("Transcript:", transcript)
        # Step 3: Add transcript as subtitles to the video
        add_text_with_ffmpeg(
            input_video_path=video_path,
            output_video_path=output_filename,
            text=transcript,
            font="Arial.ttf",  # Update with the path to a valid font
            x=50,
            y=50,
            font_size=24,
            font_color="yellow"
        )

        # Return the output video
        return FileResponse(output_filename, media_type="video/mp4", filename="processed_video.mp4")

    finally:
        # Clean up temporary files
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
        if os.path.exists(output_filename):
            os.remove(output_filename)