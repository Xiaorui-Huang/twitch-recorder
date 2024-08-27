import asyncio
import streamlink
import os
import configparser
import signal
import argparse
from datetime import datetime
from tkinter import filedialog, Tk
from time import sleep
from pathlib import Path

twitch_home = str(Path.home() / 'Downloads' / 'twitch_recordings')

# Add argparse
parser = argparse.ArgumentParser(description="Twitch stream recorder")
parser.add_argument("username", help="Twitch username of the streamer")
parser.add_argument("-l", "--list", action="store_true", help="List available stream qualities")
parser.add_argument("-q", "--quality", default="best", help="Choose stream quality (default: best)")
parser.add_argument("-o", "--output", default=twitch_home, help="Output folder path (default: ~/Downloads/twitch_recordings/<twitch_username>)")
args = parser.parse_args()

twitch_username = args.username
output_folder = args.output

config_file_path = 'config.ini'
config = configparser.ConfigParser()

# Check if the config file exists, if not create one
if not os.path.exists(config_file_path):
    config['DEFAULT'] = {'output_folder': ''}
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)

# Load the config file
config.read(config_file_path)

# If the output_folder variable in the config file is not set, or if the output folder argument is used, ask the user for input and open file explorer
if not output_folder:
    print('\nNow please choose the Folder location, in which all future recordings should be saved into.\nA window should open up soon ...')
    sleep(3)
    root = Tk()
    root.withdraw()
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    output_folder = Path(output_folder)
    root.destroy()
elif output_folder == twitch_home:
    # If default output folder is used, update config file
    config['DEFAULT']['output_folder'] = output_folder

output_folder = str(Path(output_folder) / twitch_username)

# Save the variables to the config file
with open(config_file_path, 'w') as configfile:
    config.write(configfile)

def list_stream_qualities(username):
    twitch_stream_url = f"https://www.twitch.tv/{username}"
    streams = streamlink.streams(twitch_stream_url)
    if streams:
        print("Available stream qualities:")
        for quality in streams.keys():
            print(f"➡️ {quality}")
    else:
        print("No streams available.")
    return streams

async def get_stream_url(username, quality):
    twitch_stream_url = f"https://www.twitch.tv/{username}"
    streams = streamlink.streams(twitch_stream_url)

    if not streams:
        return None
        
    if quality not in streams: 
        print(f"Requested quality '{quality}' not available. Using 'best' quality instead.")
        quality = 'best'

    stream = streams[quality]
    m3u8_url = stream.url
    print(f"Will record from {quality} livestream .m3u8 URL: {m3u8_url}")
    return m3u8_url

async def monitor_stream(username, quality):
    try:
        while True:
            m3u8_url = await get_stream_url(username, quality)
            if m3u8_url:
                await record_stream(m3u8_url)
                break
            else:
                print(f"No stream is live for {username}. Checking again in 60 seconds...")
                await asyncio.sleep(60)
    except KeyboardInterrupt:
        print("\nStream monitoring stopped by user.")

async def record_stream(m3u8_url):
    quality_suffix = "_" + args.quality if args.quality != 'best' else ''
    output_file = f'{output_folder}/{twitch_username}_{datetime.now().strftime("%d_%m_%y-%H_%M")}{quality_suffix}.mp4'
    ffmpeg_cmd = ['ffmpeg', '-i', m3u8_url, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', output_file]
    
    process = await asyncio.create_subprocess_exec(*ffmpeg_cmd, stdin=asyncio.subprocess.PIPE)
    
    print("Recording started. Press Ctrl+C to stop and finalize the recording.")
    
    try:
        await process.communicate()
    except asyncio.CancelledError:
        print("\nCtrl+C detected. Finalizing the recording...")
        # Send 'q' to FFmpeg's stdin to quit gracefully
        process.stdin.write(b'q')
        await process.stdin.drain()
        try:
            await asyncio.wait_for(process.wait(), timeout=10.0)
        except asyncio.TimeoutError:
            print("FFmpeg didn't exit in time. Terminating...")
            process.terminate()
            await process.wait()
    
    print(f"Recording finished. Output file: {output_file}")

def signal_handler(signum, frame):
    raise KeyboardInterrupt

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    
    if args.list:
        list_stream_qualities(twitch_username)
    else:
        try:
            asyncio.run(monitor_stream(twitch_username, args.quality))
        except KeyboardInterrupt:
            print("\nExiting...")
