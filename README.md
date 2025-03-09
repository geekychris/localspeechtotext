# Speech-to-Text Conversion with Vosk

This repository contains a Python script (`speech_to_text.py`) that converts spoken language in WAV audio files to text using Vosk, a lightweight offline speech recognition toolkit. The script runs entirely offline using local models without requiring internet connectivity or cloud-based services.

## System Requirements

- Raspberry Pi (3 or newer recommended) or any Linux/macOS/Windows system
- Python 3.6 or higher
- At least 200MB of free disk space for small models (larger models require 1-2GB)
- At least 512MB of RAM (1GB+ recommended)

## Installation

### 1. Installing Dependencies

Install the required Python packages:

```bash
pip install vosk soundfile numpy
```

Or if you prefer using pip3 explicitly:

```bash
pip3 install vosk soundfile numpy
```

### 2. Downloading a Vosk Model

Vosk requires a model to perform speech recognition. Models vary in size, accuracy, and language support.

#### Quick Setup (English - Small Model)

For Raspberry Pi or systems with limited resources, the small English model is recommended:

```bash
# Download the small English model
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

# Unzip the model
unzip vosk-model-small-en-us-0.15.zip

# Rename the model directory to the default name expected by the script
mv vosk-model-small-en-us-0.15 model
```

#### Alternative Models

For other languages or better accuracy, you can download different models:

- **English (larger, more accurate)**: [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) (~1.8GB)
- **French**: [vosk-model-fr-0.22](https://alphacephei.com/vosk/models/vosk-model-fr-0.22.zip)
- **German**: [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip)
- **Spanish**: [vosk-model-es-0.42](https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip)
- **Italian**: [vosk-model-it-0.22](https://alphacephei.com/vosk/models/vosk-model-it-0.22.zip)
- **Russian**: [vosk-model-ru-0.22](https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip)
- **Chinese**: [vosk-model-cn-0.22](https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip)
- **Many more**: See the [complete list of models](https://alphacephei.com/vosk/models)

When using a model different from the default, specify its path with the `--model-path` option when running the script.

## Usage

### Basic Usage

```bash
python speech_to_text.py input.wav
```

You can download the following declaration of independence as a sample file 

```bash
 wget https://monticello-www.s3.amazonaws.com/files/media/declaration.mp3
 python speech_to_text.py declaration.mp3 > declaration.txt
```

This will process `input.wav` using the default model in the `model` directory and print the recognized text.

### Advanced Usage

```bash
./speech_to_text.py --model-path /path/to/custom/model --verbose input.wav
```

#### Options:

- `--model-path PATH`: Specify a custom path to the Vosk model directory (default: "model")
- `--verbose`: Enable detailed output during processing

### Examples

1. Convert a simple announcement recording:
   ```bash
   ./speech_to_text.py recordings/announcement.wav
   ```

2. Use a Spanish model for a Spanish audio file:
   ```bash
   ./speech_to_text.py --model-path vosk-model-es-0.42 audio_espanol.wav
   ```

3. Process an interview with verbose logging:
   ```bash
   ./speech_to_text.py --verbose interview_session.wav > transcript.txt
   ```

## Supported Audio Formats

The script is designed to work with WAV files. For other formats, convert them to WAV first using tools like ffmpeg:

```bash
ffmpeg -i input.mp3 output.wav
```

## Troubleshooting

### Common Issues and Solutions

1. **"Model not found" error**
   - Ensure you've downloaded and extracted the model correctly
   - Verify the model directory path matches what's specified in the command (default is "model")

2. **"Failed to open audio file" error**
   - Verify the audio file exists and is not corrupted
   - Ensure the file is in WAV format
   - For non-WAV files, convert using ffmpeg first

3. **"ModuleNotFoundError" for vosk/soundfile/numpy**
   - Install the missing package with `pip install packagename`
   
4. **Low recognition accuracy**
   - Try using a larger model for better accuracy
   - Ensure your audio has clear speech with minimal background noise
   - Check if you're using a model for the correct language
   
5. **Script running too slowly**
   - Use a smaller model on low-powered devices like Raspberry Pi
   - Make sure you have enough RAM available

6. **Garbled or no output**
   - Check the sample rate of your audio file with `ffprobe input.wav`
   - Make sure the audio is properly formatted (16-bit PCM is recommended)
   - Convert problematic files: `ffmpeg -i input.wav -ar 16000 -ac 1 -c:a pcm_s16le output.wav`

### Memory Issues on Raspberry Pi

If you encounter memory errors on Raspberry Pi:

1. Use the smallest appropriate model (e.g., vosk-model-small-en-us-0.15)
2. Increase your swap space:
   ```bash
   # Edit the swap configuration
   sudo nano /etc/dphys-swapfile
   
   # Change CONF_SWAPSIZE to 1024
   CONF_SWAPSIZE=1024
   
   # Restart the swap service
   sudo /etc/init.d/dphys-swapfile restart
   ```

## Additional Resources

- [Vosk API Documentation](https://alphacephei.com/vosk/install)
- [Complete list of Vosk models](https://alphacephei.com/vosk/models)
- [Vosk GitHub Repository](https://github.com/alphacep/vosk-api)

## License

The script is provided as open-source software. The Vosk models have their own licensing terms, typically Apache 2.0 License.

---

For any issues not covered in this documentation, please open an issue in the repository or contribute improvements to this README.

# localspeechtotext
