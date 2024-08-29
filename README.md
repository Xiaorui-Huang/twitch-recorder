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

## The Noob Manual

**Windows**

1. Open powershell (open start menu and search it, if y'all can't find this, I literally can't help you🤣

2. Install scoop package manager by copying the following into the commandline (same instruction as in https://scoop.sh)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

3. Install python & ffmpeg & git
```powershell
scoop bucket add main
scoop install python
scoop install ffmpeg
```
4. Git code
```
git clone https://github.com/Xiaorui-Huang/twitch-recorder.git
cd twitch-recorder
```

5. Record the path to this code's directory
```
pwd # then copy the output and save it
# to get back to it do 
cd <the shit you just copy and saved>
```

6. Go to [installation](#installation) **AND always execute the commands in the code's directory**



**Mac**

Not gonna help a Mac user🙂‍↔️ 

(fine, just go to https://brew.sh/ and figure it out yourself, Mac might even have python pre-installed idk)


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

4. Press Ctrl+C to stop recording. The script will attempt to finalize the recording up to this point and save

5. Check your **Downloads** folder and Pog

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
- `-o SAVE_PATH, `--output SAVE_PATH`: Choose a custom directory to save the recordings (default: ~/Downloads/twitch_recordings)

## Configuration

On first run, you'll be prompted to choose an output folder. This path will be saved in a `config.ini` file.

## Disclaimer

Please note that recording and distributing Twitch streams without the permission of the content creator may violate Twitch's terms of service and could lead to legal consequences. Use this code responsibly and with respect for the creators whose content you are recording.

## License

[MIT License](LICENSE)
