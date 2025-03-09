"""
Speech to Text Converter

This script converts speech in a WAV file to text using the Vosk library
for offline speech recognition.

Requirements:
    - Python 3.6+
    - vosk
    - soundfile
    - numpy

Installation:
    pip install vosk soundfile numpy

Usage:
    python speech_to_text.py input.wav

    Optional arguments:
    --model-path PATH    Path to the Vosk model directory (default: "model")
    --verbose            Enable verbose output

Notes on Vosk Models:
    Before using this script, you need to download a Vosk model from:
    https://alphacephei.com/vosk/models

    For Raspberry Pi:
    1. Small models are recommended due to limited resources
    2. Download a model such as vosk-model-small-en-us-0.15
    3. Unzip the model: unzip vosk-model-small-en-us-0.15.zip
    4. Rename the directory to 'model' or specify path with --model-path
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import soundfile as sf
    import numpy as np
    from vosk import Model, KaldiRecognizer
except ImportError as e:
    print(f"Error: {e}")
    print("Please install required packages:")
    print("pip install vosk soundfile numpy")
    sys.exit(1)


def check_model_exists(model_path):
    """Check if the Vosk model exists at the specified path."""
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        print("\nDownload a model from https://alphacephei.com/vosk/models")
        print("For Raspberry Pi, a small model is recommended:")
        print("1. Download: wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
        print("2. Unzip: unzip vosk-model-small-en-us-0.15.zip")
        print("3. Rename: mv vosk-model-small-en-us-0.15 model")
        return False
    return True


def process_audio(audio_path, model_path, verbose=False):
    """Process audio file and return recognized text."""
    if verbose:
        print(f"Loading model from {model_path}...")
    
    try:
        model = Model(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
    
    if verbose:
        print(f"Processing audio file: {audio_path}")
    
    try:
        # Load audio file
        waveform, sample_rate = sf.read(audio_path)
        
        # Convert to mono if stereo
        if len(waveform.shape) > 1:
            waveform = waveform[:, 0]
        
        # Resample to 16kHz if needed
        if sample_rate != 16000:
            if verbose:
                print(f"Warning: Audio sample rate is {sample_rate}Hz, not 16000Hz. Results may be affected.")
        
        # Convert to int16 format
        waveform = (waveform * 32768).astype(np.int16)
        
        # Initialize recognizer
        rec = KaldiRecognizer(model, sample_rate)
        rec.SetWords(True)
        
        # Process audio in chunks
        chunk_size = int(sample_rate * 0.2)  # 0.2 second chunks
        results = []
        
        for i in range(0, len(waveform), chunk_size):
            chunk = waveform[i:min(i + chunk_size, len(waveform))]
            if rec.AcceptWaveform(chunk.tobytes()):
                part_result = json.loads(rec.Result())
                if 'text' in part_result and part_result['text'].strip():
                    results.append(part_result['text'])
        
        # Get final result
        final_result = json.loads(rec.FinalResult())
        if 'text' in final_result and final_result['text'].strip():
            results.append(final_result['text'])
        
        return ' '.join(results)
        
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Convert speech in WAV file to text using Vosk')
    parser.add_argument('audio_file', help='Path to the WAV audio file')
    parser.add_argument('--model-path', default='model', help='Path to the Vosk model directory')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()
    
    # Check if audio file exists
    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        return 1
    
    # Check audio file format
    if audio_path.suffix.lower() != '.wav':
        print(f"Warning: File {audio_path} may not be a WAV file. This script works best with WAV files.")
    
    # Check if model exists
    if not check_model_exists(args.model_path):
        return 1
    
    # Process audio
    text = process_audio(str(audio_path), args.model_path, args.verbose)
    
    if text:
        print("\nRecognized Text:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        return 0
    else:
        print("Failed to recognize speech in the audio file.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

