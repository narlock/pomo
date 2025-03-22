"""
Pomo - settings.py
author: narlock

This file controls reading and writing settings to
~/Documents/narlock/pomo/settings.json
"""

import ansi
import json
from pathlib import Path

SETTINGS_PATH = Path.home() / "Documents" / "narlock" / "pomo" / "settings.json"

DEFAULT_POMO = {
    "name": "Default",                                                          # The name of the custom pomo setting.
    "focusTime": 1500,                                                          # The amount of time in seconds a focus session will be.
    "shortBreak": True,                                                         # Indicates that regular breaks after sessions are enabled.
    "shortBreakTime": 300,                                                      # The amount of time in seconds a break will be.
    "sessionCount": 1,                                                          # The number of sessions in the pomodoro.
    "longBreak": False,                                                         # Indicates that long break is enabled.
    "longBreakTime": 900,                                                       # The amount of time in seconds a long break will be.
    "longBreakAfterSessions": [],                                               # The break indices that will use longBreakTime over breakTime.
    "autoStartNextSession": False,                                              # Automatically starts the next focus session after a break ends. No sound or flash will play
    "autoStartBreak": False,                                                    # Automatically starts a break after a focus session ends.
    "playAlarmSound": False,                                                    # Plays an alarm sound after the countdown timer is finished.
    "alarmSound": "Default",                                                    # The alarm sound path. If "Default", will point to /sfx/DEFAULT_ALARM.wav
    "timerEndFlash": True,                                                      # Flashes the timer after the countdown timer is finished.
    "sessionMessage": "Session ${current_session} / ${total_sessions}",         # The subtext message during a focus session.
    "breakMessage": "Break ${current_session} / ${total_sessions}",             # The subtext message during a break.
    "longBreakMessage": "Long Break ${current_session} / ${total_sessions}",    # The subtext message during a long break
    "borderColor": "RED",
    "timeColor": "YELLOW",
    "subtextColor": "BLUE"
}

TEST_POMO = {
   "name": "Test",                                                              # The name of the custom pomo setting.
    "focusTime": 1,                                                             # The amount of time in seconds a focus session will be.
    "shortBreak": True,                                                         # Indicates that regular breaks after sessions are enabled.
    "shortBreakTime": 2,                                                        # The amount of time in seconds a break will be.
    "sessionCount": 3,                                                          # The number of sessions in the pomodoro.
    "longBreak": True,                                                         # Indicates that long break is enabled.
    "longBreakTime": 5,                                                       # The amount of time in seconds a long break will be.
    "longBreakAfterSessions": [2],                                               # The break indices that will use longBreakTime over breakTime.
    "autoStartNextSession": False,                                              # Automatically starts the next focus session after a break ends. No sound or flash will play
    "autoStartBreak": False,                                                    # Automatically starts a break after a focus session ends.
    "playAlarmSound": False,                                                    # Plays an alarm sound after the countdown timer is finished.
    "alarmSound": "Default",                                                    # The alarm sound path. If "Default", will point to /sfx/DEFAULT_ALARM.wav
    "timerEndFlash": True,                                                      # Flashes the timer after the countdown timer is finished.
    "sessionMessage": "Session ${current_session} / ${total_sessions}",         # The subtext message during a focus session.
    "breakMessage": "Break ${current_session} / ${total_sessions}",             # The subtext message during a break.
    "longBreakMessage": "Long Break ${current_session} / ${total_sessions}",    # The subtext message during a long break
    "borderColor": "RED",
    "timeColor": "YELLOW",
    "subtextColor": "BLUE"
}

INITIAL_SETTINGS = {
    "mainMenu": {
        "title": "POMO",
        "borderColor": "RED",
        "timeColor": "YELLOW",
        "subtextColor": "BLUE"
    },
    "previousPomoName": "Default",
    "pomos": [
        DEFAULT_POMO, TEST_POMO
    ],
    "countdown": {                                                          # The setting used for instant countdown timer.
        "autoEndCountdown": False,                                          # Ends the program immediately aftee the countdown timer is completed. (No ACK)
        "timerEndFlash": True,
        "playAlarmSound": True,
        "alarmSound": "Default",
        "message": "Focusing...",
        "borderColor": "RED",
        "timeColor": "YELLOW",
        "subtextColor": "BLUE"
    },
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
                                    "focusTime": 0,
                                    "breakTime": 0
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
        print(f"\n{ansi.GREEN}{ansi.BOLD}Settings updated successfully.{ansi.RESET}")
    except Exception as e:
        print(f"{ansi.RED}{ansi.BOLD}Error updating settings: {e}{ansi.RESET}")

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

def get_pomo(user_settings = load_settings(), name: str = "Default"):
    """
    Retrieves a pomo by its name. By default, it will search for the
    pomo with the name of "Default"
    """
    for pomo in user_settings.get("pomos", []):
        if pomo.get("name") == name:
            return pomo

    # No pomo with `name` was found.   
    return None

def get_pomo_index_by_name(user_settings = load_settings(), name: str = "Default"):
    """
    Retrieves a pomo index by its name.
    """
    for index, pomo in enumerate(user_settings.get("pomos", [])):
        if pomo.get("name") == name:
            return index

    # No pomo with `name` was found.   
    return -1

def get_list_of_pomo_names(user_settings = load_settings()):
    """
    Returns a list of strings containing each pomo name.
    """
    names = []
    for pomo in user_settings.get("pomos", []):
        if pomo.get("name"):
            names.append(pomo.get("name"))
    
    return names

def make_countdown_pomo(focusTime: int, global_settings = load_settings()):
    countdown = global_settings.get('countdown')
    return {
        "name": "OneTimePomo",
        "focusTime": focusTime,
        "shortBreak": False,
        "shortBreakTime": 0,
        "sessionCount": 1,
        "longBreak": False,
        "longBreakTime": 0,
        "longBreakAfterSessions": [],
        "autoStartNextSession": countdown['autoEndCountdown'],
        "autoStartBreak": False,
        "playAlarmSound": countdown['playAlarmSound'],
        "alarmSound": "Default",
        "timerEndFlash": countdown['timerEndFlash'],
        "sessionMessage": countdown['message'],
        "breakMessage": "Break ${current_session} / ${total_sessions}",
        "longBreakMessage": "Long Break ${current_session} / ${total_sessions}",
        "borderColor": countdown['borderColor'],
        "timeColor": countdown['timeColor'],
        "subtextColor": countdown['subtextColor']
    }

def set_previous_pomo(name: str, global_settings = load_settings()):
    global_settings['previousPomoName'] = name
    update_settings(global_settings)