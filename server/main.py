import os
import tempfile
import subprocess
import requests
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

FFMPEG_BIN = os.getenv("FFMPEG_BIN", "ffmpeg")
WHISPER_SERVER = os.getenv("WHISPER_SERVER", "http://localhost:8080/inference")
BUFFER_SIZE = int(os.getenv("BUFFER_SIZE", "200000"))


@app.get("/")
def health():
    return {"status": "ok"}


def convert_to_wav(input_path: str) -> str:
    output_path = input_path + ".wav"

    subprocess.run(
        [
            FFMPEG_BIN,
            "-y",
            "-i",
            input_path,
            "-ar",
            "16000",
            "-ac",
            "1",
            output_path,
        ],
        check=True,
    )

    return output_path


def transcribe_audio(wav_path: str) -> str:
    try:
        with open(wav_path, "rb") as f:
            r = requests.post(
                WHISPER_SERVER,
                files={"file": f},
                timeout=60
            )

        if r.status_code != 200:
            print("Whisper error:", r.text)
            return ""

        return r.json().get("text", "")

    except Exception as e:
        print("Transcription error:", e)
        return ""


@app.websocket("/ws/audio")
async def audio_stream(ws: WebSocket):
    await ws.accept()
    print("WebSocket connected")

    buffer = bytearray()

    try:
        while True:
            chunk = await ws.receive_bytes()
            buffer.extend(chunk)

            # process audio when buffer reaches threshold
            if len(buffer) > BUFFER_SIZE:

                with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
                    f.write(buffer)
                    webm_path = f.name

                buffer.clear()

                print("Saved chunk:", webm_path)

                wav_path = convert_to_wav(webm_path)

                print("Converted wav:", wav_path)

                transcript = transcribe_audio(wav_path)

                print("Transcript:", transcript)

                await ws.send_text(transcript)

                # cleanup temp files
                os.remove(webm_path)
                os.remove(wav_path)

    except WebSocketDisconnect:
        print("Client disconnected")

    except Exception as e:
        print("WebSocket error:", e)