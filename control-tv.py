#!/usr/bin/env python3
import subprocess
import plistlib
import time
import asyncio
import threading
from bscpylgtv import WebOsClient
from pynput import keyboard

# Your settings
IP = '192.168.68.110'
Input = 'HDMI_1'
Input_Mode = 'pc'
Input_Name = 'Mac Studio'

# Create an asyncio event loop
loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)


# Global WebOsClient instance and a lock for thread safety
client = None
client_lock = asyncio.Lock()
disconnect_timer = None


async def ensure_connected():
    global client, disconnect_timer
    async with client_lock:
        if client is None:
            client = await WebOsClient.create(IP, states=[])
            await client.connect()
        if disconnect_timer is not None:
            disconnect_timer.cancel()
        disconnect_timer = loop.call_later(
            10, lambda: asyncio.run_coroutine_threadsafe(disconnect_client(), loop))


async def disconnect_client():
    global client
    async with client_lock:
        if client is not None:
            await client.disconnect()
            client = None


async def change_display_settings():
    await ensure_connected()
    await client.set_device_info(Input, Input_Mode, Input_Name)


async def volume_up():
    await ensure_connected()
    await client.volume_up()


async def volume_down():
    await ensure_connected()
    await client.volume_down()

async def mute():
    await ensure_connected()
    muted = await client.get_muted()
    await client.set_mute(not muted)

async def volume_control(key):
    if key == keyboard.Key.media_volume_up:
        await volume_up()
    elif key == keyboard.Key.media_volume_down:
        await volume_down()
    elif key == keyboard.Key.media_volume_mute:
        await mute()

def on_press(key):
    if control_audio:  # Check if the TV is selected as the audio device
        asyncio.run_coroutine_threadsafe(volume_control(key), loop)


def run_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def is_display_connected():
    cmd = ["system_profiler", "SPDisplaysDataType", "-xml"]
    output = subprocess.check_output(cmd)

    # Parse the plist XML output
    plist = plistlib.loads(output)

    # Extract the model number of the primary display
    for display in plist[0]['_items'][0]['spdisplays_ndrvs']:
        name = display["_name"]
        if name.startswith("LG TV"):
            return True
    return False


def is_audio_selected():
    cmd = ["system_profiler", "SPAudioDataType", "-xml"]
    output = subprocess.check_output(cmd)

    # Parse the plist XML output
    plist = plistlib.loads(output)

    for device in plist[0]['_items'][0]['_items']:
        if device["_name"].startswith("LG TV") and 'coreaudio_default_audio_output_device' in device.keys():
            return True
    return False


# Run the keyboard listener in a separate thread
listener_thread = threading.Thread(target=run_keyboard_listener)
listener_thread.start()


async def main_loop():
    global control_audio
    connected = False
    while True:
        # Activate or deactivate the volume events here
        control_audio = is_audio_selected()
        try:
            got_connected = is_display_connected()
            if not connected and got_connected:
                await change_display_settings()
            connected = got_connected
        except Exception as e:
            print(f"Error: {e}")
            connected = False
        await asyncio.sleep(5)

# Run the main loop
loop.run_until_complete(main_loop())
