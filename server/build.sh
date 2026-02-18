#!/usr/bin/env bash
set -e

echo "Installing system dependencies..."
apt-get update
apt-get install -y ffmpeg build-essential cmake git

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Cloning whisper.cpp..."
if [ ! -d "whisper.cpp" ]; then
  git clone https://github.com/ggerganov/whisper.cpp
fi

echo "Building whisper..."
cd whisper.cpp
make

echo "Downloading model..."
bash models/download-ggml-model.sh base.en

echo "Build complete."
