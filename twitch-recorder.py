import asyncio
from pathlib import Path
import streamlink
import os
import configparser
import signal
import argparse
import requests
from datetime import datetime
from tkinter import filedialog, Tk
from time import sleep

# Set up the default twitch recordings folder

# Add argparse
parser = argparse.ArgumentParser(description="Twitch stream recorder")
parser.add_argument("username", help="Twitch username of the streamer")
parser.add_argument("-l", "--list", action="store_true", help="List available stream qualities")
parser.add_argument("-q", "--quality", default="best", help="Choose stream quality (default: best)")
parser.add_argument("-o", "--output", default="", help="Output folder path")
parser.add_argument(
    "-d", "--delay", type=int, default=300, help="Retry delay in seconds if stream is not live (default: 300 seconds)"
)
parser.add_argument("-s", "--subscribe", nargs="?", const=True, help="Subscribe to a ntfy topic for live notifications")
args = parser.parse_args()


def print_red(*args, **kwargs):
    print("\033[91m", end="")
    print(*args, **kwargs)
    print("\033[0m", end="")


config_file_path = "config.ini"
config = configparser.ConfigParser()

# Check if the config file exists, if not create one
if not os.path.exists(config_file_path):
    config["DEFAULT"] = {"output_folder": "", "ntfy_topic": ""}
    with open(config_file_path, "w") as configfile:
        config.write(configfile)

# Load the config file
config.read(config_file_path)

# If the output_folder variable in the config file is not set, or if the output folder argument is used, ask the user for input and open file explorer
if not args.output and not config["DEFAULT"]["output_folder"]:
    print(
        "\nNow please choose the Folder location, in which all future recordings should be saved into.\nA window should open up soon ..."
    )
    sleep(3)
    root = Tk()
    root.withdraw()
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    root.destroy()
    config["DEFAULT"]["output_folder"] = output_folder

# output folder with username
output_folder = os.path.join(
    config["DEFAULT"]["output_folder"], args.username
)  # Save recordings in a folder named after the streamer

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Handle ntfy topic subscription
ntfy_topic = None
if args.subscribe is not None:
    if args.subscribe is True:
        ntfy_topic = config["DEFAULT"].get("ntfy_topic", "")
        if not ntfy_topic:
            ntfy_topic = input("No ntfy topic found in the config. Please enter the ntfy topic: ")
            config["DEFAULT"]["ntfy_topic"] = ntfy_topic
    else:
        ntfy_topic = args.subscribe
        config["DEFAULT"]["ntfy_topic"] = ntfy_topic

# Save the variables to the config file
with open(config_file_path, "w") as configfile:
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


async def get_stream_url(username, quality, retries=5, delay=30):
    twitch_stream_url = f"https://www.twitch.tv/{username}"
    streams = streamlink.streams(twitch_stream_url)

    # get streams with retries
    for i in range(retries):
        try:
            streams = streamlink.streams(twitch_stream_url)
            if streams:
                break
        except streamlink.exceptions.PluginError as e:
            print(f"Attempt {i+1}/{retries} failed: {e}. Retrying in {delay} seconds...")
            sleep(delay)

    if not streams:
        return None

    if quality not in streams:
        print(f"Requested quality '{quality}' not available. Using 'best' quality instead.")
        quality = "best"

    stream = streams[quality]
    m3u8_url = stream.url
    print(f"Will record from {quality} livestream .m3u8 URL: \n\n{m3u8_url}\n")
    return m3u8_url


async def monitor_stream(username, quality):
    try:
        while True:
            m3u8_url = await get_stream_url(username, quality)
            if m3u8_url:
                await record_stream(m3u8_url, username)
                break
            else:
                delay = args.delay
                print(f"No stream is live for {username}. Checking again in {delay} seconds...")
                await asyncio.sleep(delay)
    except KeyboardInterrupt:
        print("\nStream monitoring stopped by user.")


async def record_stream(m3u8_url, username):
    quality_suffix = "_" + args.quality if args.quality != "best" else ""
    output_file = f'{output_folder}/{username}_{datetime.now().strftime("%m_%d_%y-%H_%M_%S")}{quality_suffix}.mp4'
    ffmpeg_cmd = ["ffmpeg", "-i", m3u8_url, "-c", "copy", "-bsf:a", "aac_adtstoasc", output_file]

    print_red("Recording started 🖥️ 🕹️ 📽️. Press Ctrl+C to stop and finalize the recording.")

    process = await asyncio.create_subprocess_exec(
        *ffmpeg_cmd, stdin=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    if ntfy_topic:
        send_ntfy_notification(ntfy_topic, f"Recording of {username} stream started.")

    try:
        while process.returncode is None:
            line_err = await process.stderr.readline()
            if line_err == b"":
                break
            decoded_line = line_err.decode("utf-8", errors="ignore")

            # Split the line by '\r' and filter for 'size='
            if decoded_line.startswith("size="):
                r_index = decoded_line.find("\r")
                info = decoded_line[:r_index] if r_index != -1 else decoded_line.rstrip("\n")
                print(info, end="\r", flush=True)

        await process.wait()

    except asyncio.CancelledError:
        print("\nCtrl+C detected. Finalizing the recording...")
        # Send 'q' to FFmpeg's stdin to quit gracefully
        process.stdin.write(b"q")
        await process.stdin.drain()
        try:
            await asyncio.wait_for(process.wait(), timeout=10.0)
        except asyncio.TimeoutError:
            print("FFmpeg didn't exit in time. Terminating...")
            process.terminate()
            await process.wait()

    print_red(f"Recording finished. Output file: {os.path.abspath(output_file)}", flush=True)

    if ntfy_topic:
        send_ntfy_notification(ntfy_topic, f"Recording of {username} stream finished. Output file: {output_file}")


def send_ntfy_notification(topic, message):
    url = f"https://ntfy.sh/{topic}"
    response = requests.post(url, data=message)
    if response.status_code == 200:
        print(f"Notification sent to ntfy topic: {topic}")
    else:
        print(f"Failed to send notification. HTTP Status Code: {response.status_code}")


def signal_handler(signum, frame):
    raise KeyboardInterrupt


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    if args.list:
        list_stream_qualities(args.username)
    else:
        try:
            asyncio.run(monitor_stream(args.username, args.quality))
        except KeyboardInterrupt:
            print("\nExiting...")
