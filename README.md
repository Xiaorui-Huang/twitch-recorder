# Twitch Stream Recorder

This Python script allows you to record Twitch streams using Streamlink and FFmpeg. It provides options to list available stream qualities and choose a specific quality for recording.

## Features

- Record Twitch streams in various qualities
- List available stream qualities
- Automatically retry if the stream is not live
- Saving of recording in process with Ctrl+C

## Requirements

- Python 3.7+
- Streamlink
- FFmpeg

## Installation

1. Clone this repository or download the script.
2. Install the required Python packages:

   ```
   pip install streamlink asyncio
   ```

3. Ensure FFmpeg is installed and available in your system PATH.

## Quick Start

1. Run the script with a Twitch username:

   ```
   python twitch_recorder.py <username>
   ```

   This will start recording the stream in the best available quality.

2. To list available stream qualities:

   ```
   python twitch_recorder.py <username> -l
   ```

3. To record with a specific quality:

   ```
   python twitch_recorder.py <username> -q 720p
   ```

4. Press Ctrl+C to stop recording. The script will attempt to finalize the recording gracefully.

## Usage

```
python twitch_recorder.py [-h] [-l] [-q QUALITY] username
```

Positional arguments:

- `username`: Twitch username of the streamer

Optional arguments:

- `-h`, `--help`: Show help message and exit
- `-l`, `--list`: List available stream qualities
- `-q QUALITY`, `--quality QUALITY`: Choose stream quality (default: best)

## Configuration

On first run, you'll be prompted to choose an output folder. This path will be saved in a `config.ini` file.

## Disclaimer

Please note that recording and distributing Twitch streams without the permission of the content creator may violate Twitch's terms of service and could lead to legal consequences. Use this code responsibly and with respect for the creators whose content you are recording.

## License

[MIT License](LICENSE)
