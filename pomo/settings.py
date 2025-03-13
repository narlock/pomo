"""
Pomo - settings.py
author: narlock

This file controls reading and writing settings to
~/Documents/narlock/pomo/settings.json
"""

import json

DEFAULT_POMO = {
    "name": "Default",                                                      # The name of the custom pomo setting.
    "focusTime": 25,                                                        # The amount of time in minutes a focus session will be.
    "breakTime": 5,                                                         # The amount of time in minutes a break will be.
    "sessionCount": 1,                                                      # The number of sessions in the pomodoro.
    "longBreak": False,                                                     # Indicates that long break is enabled.
    "longBreakTime": 15,                                                    # The amount of time in minutes a long break will be.
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
    "previousPomo": DEFAULT_POMO,
    "pomos": [
        {
            DEFAULT_POMO
        }
    ]
}

"""
Called when there is no settings.json, this function
will create the initial settings inside of a newly
created settings.json file. For whatever reason,
if the settings.json file is tampered with, a
suggestion to reset to default will be available
and will call this function.
"""
def write_initial_settings():
    pass

