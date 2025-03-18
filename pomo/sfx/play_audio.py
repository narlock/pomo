"""
play_audio - Pomo
author: narlock

This file plays and kills audio processes.
Pomo will play audio processes using afplay or aplay.
These methods have capability to kill all processes that
are using both methods to play audio.
"""

import sys
import os
import signal
import subprocess

process_id_list = []

def play_sound():
    file_path = os.path.join(os.path.dirname(__file__), "DEFAULT_ALARM.wav")
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found!")
        return

    process = None
    try:
        if sys.platform == 'darwin':  # macOS
            process = subprocess.Popen(["afplay", file_path])
        else:  # Linux
            process = subprocess.Popen(["aplay", file_path])

        # Add the process ID to process_id_list so we can kill it later
        if process:
            process_id_list.append(process.pid)
            print(f"Sound process with pid {process.pid} added to process_id_list...")

        # process.wait()
    except Exception as e:
        print(f"Error playing sound: {e}")

def kill_processes():
    for pid in process_id_list:
        print(f"Attempting to kill process {pid}")
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Successfully killed process {pid}")
        except ProcessLookupError:
            print(f"Process {pid} not found (may have already exited).")