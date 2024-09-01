# Twitch Stream Recorder <img src="images/cool-hacker-pepe.gif" alt="KEKW emote" width="100">

This Python script allows you to record Twitch streams using Streamlink and FFmpeg. It provides options to list available stream qualities, choose a specific quality for recording, and automatically retry if the stream is not live.

<img src="images/twitch-emote-twerking-ban-ceo-dan-clancy.jpg" alt="twerk on ceo dan clancy - emote" width="700">

*Tested on a raspberry pi 4 and barely noticed if any resources are used up, thanks **ffmpeg***

**Wanna learn how to code this shit?** [Check here](#license)

## Features

<img src="images/twichemotesss.jpg" alt="stupid twitch banner" width="300">

- Record Twitch streams
- Auto Live Monitoring
- Choose your stream recording qualities/resolutions
- Save recordings early with Ctrl+C
- Subscribe to streamer and get notified when they go live (requires [`ntfy`](https://ntfy.sh))

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

(Fine, just go to [https://brew.sh/](https://brew.sh/) and figure it out yourself, just use `brew` instead of `scoop`. Mac might even have Python pre-installed, idk.)

**Linux**

You guys are computer wizards, donno why you are here reading this...

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

5. **To End The Recording Early** press  Ctrl+C to stop recording. The script will attempt to finalize the recording up to this point and save it.

6. Sit back, go do your stuff, sip some coffee and binge steamer later.

    ![Pog](images/pogchamp-pog.gif)

## Usage

```bash
python twitch_recorder.py [-h] [-l] [-q QUALITY] [-d DELAY] [-s NTFY_TOPIC] [-o SAVE_PATH] username
```

### Positional arguments

- `username`: Twitch username of the streamer

### Optional arguments

- `-h`, `--help`: Show help message and exit
- `-l`, `--list`: List available stream qualities
- `-q QUALITY`, `--quality QUALITY`: Choose stream quality (default: best)
- `-d DELAY`, `--delay DELAY`: Set retry delay in seconds to recheck for live (default: 300 seconds)
- `-o SAVE_PATH`, `--output SAVE_PATH`: Choose a custom directory to save the recordings, (will pop up a file selector for the first time, change it in `config.ini` later)
- `-s`, `--subscribe`: Subscribe to the streamer and get a [ntfy.sh](https://ntfy.sh) notification when they go live (requires `ntfy` and subscription to your `topic` of choice)

## Configuration

On the first run, you'll be prompted to choose an output folder. This path will be saved in a `config.ini` file for future runs.

Same thing if you want to subscribe to a streamer, it will prompt you for a `topic` to subscribe to and save it in the `config.ini` file.

## Disclaimer

Please note that recording and distributing Twitch streams without the permission of the content creator may violate Twitch's terms of service and could lead to legal consequences. Use this code responsibly and with respect for the creators whose content you are recording.

## License

[MIT License](LICENSE)

![delulu](images/delulu-hacker-pepe.gif)
