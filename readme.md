## To install dependencies

pip install fastapi uvicorn python-multipart moviepy whisper

## To start the server

uvicorn app:app --host 0.0.0.0 --port 8000

## To request 

curl -X POST "http://127.0.0.1:8000/process-video/" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "file=sample.mp4" \
--output processed_video.mp4


## To run only the transcriber

phython3 video_transcriber.py

