from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import tempfile
import subprocess

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}


def convert_to_wav(input_path):
    output_path = input_path + ".wav"

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ])

    return output_path


def transcribe_audio(wav_path):
    result = subprocess.run(
        [
            "./whisper.cpp/build/bin/whisper-cli",
            "-m",
            "./whisper.cpp/models/ggml-base.en.bin",
            "-f",
            wav_path
        ],
        capture_output=True,
        text=True
    )

    print("Whisper output:\n", result.stdout)
    print("Whisper errors:\n", result.stderr)

    return result.stdout


@app.websocket("/ws/audio")
async def audio_stream(ws: WebSocket):
    await ws.accept()
    print("WebSocket connected")

    audio_data = b""

    try:
        while True:
            chunk = await ws.receive_bytes()
            print("Received chunk:", len(chunk))
            audio_data += chunk

    except WebSocketDisconnect:
        print("Client disconnected")

    except Exception as e:
        print("Error:", e)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
        f.write(audio_data)
        webm_path = f.name

    print("Saved audio:", webm_path)

    wav_path = convert_to_wav(webm_path)
    print("Converted to WAV:", wav_path)

    transcript = transcribe_audio(wav_path)
    print("Transcript:\n", transcript)
