# Twitch Stream Recorder

This Python script allows you to record Twitch streams using Streamlink and FFmpeg. It provides options to list available stream qualities, choose a specific quality for recording, and automatically retry if the stream is not live.

## Features

- Record Twitch streams
- Run in the background and auto record once streamer is live
- List available stream qualities
- Save recordings still in progress with Ctrl+C

## Requirements

- Python 3.7+
- Streamlink
- FFmpeg

## The Noob Manual

**Windows**

1. Open PowerShell (open the Start menu and search for it. If you can't find this, I literally can't help you🤣).

2. Install the Scoop package manager by copying the following into the command line (same instructions as in [https://scoop.sh](https://scoop.sh)):
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
    ```

3. Install Python, FFmpeg, and Git:
    ```powershell
    scoop bucket add main
    scoop install python ffmpeg git
    ```

4. Clone the code repository:
    ```powershell
    git clone https://github.com/Xiaorui-Huang/twitch-recorder.git
    cd twitch-recorder
    ```

5. Record the path to this code's directory:
    ```powershell
    pwd  # then copy the output and save it

    # to get back to it later, use:
    cd <the path you just copied and saved>
    ```

6. Proceed to [Installation](#installation) **AND always execute the commands in the code's directory**.

**Mac**

Not gonna help a Mac user🙂‍↔️ 

(Fine, just go to [https://brew.sh/](https://brew.sh/) and figure it out yourself. Mac might even have Python pre-installed, idk.)

## Installation

1. Clone this repository or download the script.
2. Install the required Python packages:
    ```bash
    pip install streamlink asyncio
    ```
3. Ensure FFmpeg is installed and available in your system PATH.

## Quick Start

1. Run the script with a Twitch username:
    ```bash
    python twitch_recorder.py <username>
    ```
    This will start recording the stream in the best available quality.

2. To list available stream qualities:
    ```bash
    python twitch_recorder.py <username> -l
    ```

3. To record with a specific quality:
    ```bash
    python twitch_recorder.py <username> -q 720p
    ```

4. To customize the retry delay (default is 5 minutes):
    ```bash
    python twitch_recorder.py <username> -r 600  # Retry every 10 minutes
    ```

5. Press Ctrl+C to stop recording. The script will attempt to finalize the recording up to this point and save it.

6. Check your **Downloads** folder and Pog.

## Usage

```bash
python twitch_recorder.py [-h] [-l] [-q QUALITY] [-d DELAY] [-o SAVE_PATH] username
```

### Positional arguments:

- `username`: Twitch username of the streamer

### Optional arguments:

- `-h`, `--help`: Show help message and exit
- `-l`, `--list`: List available stream qualities
- `-q QUALITY`, `--quality QUALITY`: Choose stream quality (default: best)
- `-d DELAY`, `--delay DELAY`: Set retry delay in seconds if stream is not live (default: 300 seconds)
- `-o SAVE_PATH`, `--output SAVE_PATH`: Choose a custom directory to save the recordings (default: ~/Downloads/twitch_recordings)

## Configuration

On the first run, you'll be prompted to choose an output folder. This path will be saved in a `config.ini` file for future runs.

## Disclaimer

Please note that recording and distributing Twitch streams without the permission of the content creator may violate Twitch's terms of service and could lead to legal consequences. Use this code responsibly and with respect for the creators whose content you are recording.

## License

[MIT License](LICENSE)
