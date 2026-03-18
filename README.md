# Stand
A simple meeting transcriber for web based meetings


> “Run the build script, then start server, then continue extension work.”

---

# README — Resume Guide (Backend Ready)

## Project State

Backend transcription pipeline is working.

* WebSocket audio endpoint implemented
* Audio saved and converted via ffmpeg
* whisper.cpp built via build script
* Transcription confirmed
* Extension not started yet

Next task:

→ Build browser extension for audio capture

---

# How to Resume Work

## 1. Pull latest code

```
git pull
```

---

## 2. Run build script

From `server`:

```
bash build.sh
```

This will:

* Install system dependencies
* Clone whisper.cpp if missing
* Build whisper
* Download model

No manual setup required.

---

## 3. Run server

```
uvicorn main:app --host 0.0.0.0 --port 8000
```

Check:

```
http://localhost:8000
```

Should return:

```
{"status":"ok"}
```

---

# WebSocket Endpoint

```
/ws/audio
```

Used by extension to stream audio.

---

# Backend Flow

```
Audio → WebSocket → Save → Convert → Whisper → Transcript
```

---

# Confirm Whisper Works

Optional check:

```
cd whisper.cpp
cd whisper.cpp
./build/bin/whisper-cli -m models/ggml-base.en.bin -f samples/jfk.wav
```

---

# Next Step — Extension Work

When returning, start here:

1. Create Chrome extension
2. Capture tab audio
3. Stream chunks to backend
4. Verify transcript after recording

Goal:

```
Meeting → extension → backend → transcript
```

---

# Important Notes

* Do not commit model files
* build.sh handles setup
* ffmpeg required
* Paths assume whisper inside server folder

---

# Project Structure

```
server/
  main.py
  build.sh
  whisper.cpp/
extension/ (next work)
```

---

# Where I Left Off

Backend stable.

Ready to begin extension implementation.

---

If you want, I can add a really useful section called:

## “When things break”

with quick fixes like:

* ffmpeg errors
* model missing
* build failures
* websocket issues
* render deploy quirks


