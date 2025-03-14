"""
Pomo - settings.py
author: narlock

This file controls reading and writing settings to
~/Documents/narlock/pomo/settings.json
"""

import json
import os
from pathlib import Path

SETTINGS_PATH = Path.home() / "Documents" / "narlock" / "pomo" / "settings.json"

DEFAULT_POMO = {
    "name": "Default",                                                      # The name of the custom pomo setting.
    "focusTime": 1500,                                                      # The amount of time in seconds a focus session will be.
    "shortBreak": True,                                                     # Indicates that regular breaks after sessions are enabled.
    "shortBreakTime": 300,                                                       # The amount of time in seconds a break will be.
    "sessionCount": 1,                                                      # The number of sessions in the pomodoro.
    "longBreak": False,                                                     # Indicates that long break is enabled.
    "longBreakTime": 900,                                                   # The amount of time in seconds a long break will be.
    "longBreakAfterSessions": [],                                           # The break indices that will use longBreakTime over breakTime.
    "autoStartNextSession": False,                                          # Automatically starts the next focus session after a break ends.
    "autoStartBreak": False,                                                # Automatically starts a break after a focus session ends.
    "playAlarmSound": False,                                                # Plays an alarm sound after the countdown timer is finished.
    "alarmSound": "Default",                                                # The alarm sound path. If "Default", will point to /sfx/DEFAULT_ALARM.wav
    "timerEndFlash": True,                                                  # Flashes the timer after the countdown timer is finished.
    "sessionMessage": "Session {$current_session} / {$total_sessions}",     # The subtext message during a focus session.
    "breakMessage": "Break {$current_session} / {$total_sessions}",         # The subtext message during a break.
    "pauseAllowed": False,                                                  # Allows the user to pause the timer during focus sessions and breaks.
    "adminMode": False,                                                     # Allows the user to freely change components of the pomodoro while it is in progress.
    "color": {
        "border": "RED",                                                    # The color of the timer's border.
        "time": "YELLOW",                                                   # The color of the timer's text.
        "subtext": "BLUE"                                                   # The color of the subtext displayed below the timer.
    },
}

INITIAL_SETTINGS = {
    "title": "POMO",
    "previousPomoName": "Default",
    "pomos": [
        DEFAULT_POMO
    ],
    "currentFocusStreak": 0,
    "longestFocusStreak": 0,
    "totalNumberOfSessions": 0,
    "totalNumberOfBreaks": 0,
    "totalFocusTime": 0,
    "year": {
        2025: {
            "longestFocusStreak": 0,
            "totalNumberOfSessions": 0,
            "totalNumberOfBreaks": 0,
            "totalFocusTime": 0,
            "totalBreakTime": 0,
            "month": {
                1: {
                    "totalNumberOfSessions": 0,
                    "totalNumberOfBreaks": 0,
                    "totalFocusTime": 0,
                    "totalBreakTime": 0,
                    "day": {
                        1: {
                            "totalNumberOfSessions": 0,
                            "totalNumberOfBreaks": 0,
                            "totalFocusTime": 0,
                            "totalBreakTime": 0,
                            "sessions": [
                                {
                                    "startTime": "8:00",
                                    "endTime": "9:00",
                                    "focusTime": 50,
                                    "breakTime": 10
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
}

def write_initial_settings():
    """
    Called when there is no settings.json, this function
    will create the initial settings inside of a newly
    created settings.json file. For whatever reason,
    if the settings.json file is tampered with, a
    suggestion to reset to default will be available
    and will call this function.
    """
    settings_dir = SETTINGS_PATH.parent
    settings_dir.mkdir(parents=True, exist_ok=True)
    
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(INITIAL_SETTINGS, f, indent=4)
    print("Initial settings.json file created.")

def update_settings(settings):
    """
    Updates the settings.json file with an updated
    settings object.
    """
    try:
        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4)
        print("Settings updated successfully.")
    except Exception as e:
        print(f"Error updating settings: {e}")

def load_settings():
    """
    Reads settings from $HOME/Documents/narlock/pomo/settings.json.
    If any of the directories or paths do not exist, we will run
    write_initial_settings function, and then reload our settings.
    """
    if not SETTINGS_PATH.exists():
        print("Settings file not found. Creating initial settings.")
        write_initial_settings()
    
    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading settings: {e}. Resetting to default.")
        write_initial_settings()
        return INITIAL_SETTINGS
