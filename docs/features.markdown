---
layout: page
title: Features
permalink: /features/
---
<time>Mar 22, 2025</time>

This page will highlight the current features that are in Pomo.

## Interaction
Pomo can be interacted with through simple terminal commands and through interactive terminal interfaces. This gives users flexibility in how they want to utilize the application.

Entering `pomo` into the terminal will display the main menu interactive terminal interface:

<p align="center">
  <img src="./mainMenu.png" alt="Main Menu">
</p>

Alternatively, functionality can be access directly through the command line. Entering `pomo -help` will display the different operations available directly from the command line:

<p align="center">
  <img src="./help.png" alt="Help">
</p>

If interactions are performed through the interactive interface, interactions such as "going back" or "completing a pomodoro" will result in returning back to the interactive interface. Likewise, if the interaction is performed directly through the command line, they will terminate the program. The general way to go back in the program is to use the cominbation of `CTRL + C` on the keyboard.

## Create a custom Pomo
Using `pomo -n` in the terminal will launch the new pomo creation screen. This is also accessible in the main menu. This screen is where users can customize a new pomo.

<p align="center">
  <img src="./create.png" alt="Create">
</p>

Controls while creating a pomo:
- Use the `UP` and `DOWN` arrow keys to navigate between each attribute of the pomo.
- Editing specific fields:
  - `str` (`name`, `alarmSound`, `sessionMessage`, `breakMessage`, and `longBreakMessage`): Use your keyboard to write a text string for each of the fields. (Note: `alarmSound` is currently not implemented as of v1.0.0, but instead "Default" is the only available value...)
  - `int` (`focusTime`, `shortBreakTime`, `sessionCount`, `longBreakTime`): Use your keyboard to enter in a number. For time related integers, these times are the amount of time in seconds.
  - `bool` (`shortBreak`, `longBreak`, `autoStartNextSession`, `autoStartBreak`, `playAlarmSound`, `timerEndFlash`): Use the `LEFT` and `RIGHT` arrow keys to change values between True and False.
  - `longBreakAfterSessions`: Use your keyboard to enter in numbers for the session numbers to use the long break. To enter another session number, use the `,` key on the keyboard. To delete sessions from the list, use the `backspace` key.

## Edit a custom Pomo
After a pomo has been created, you can change its settings by using `pomo -e <pomo_name>`, where "pomo_name" is the `name` value that you gave to your pomo. The edit mode can be accessed from the interactive menu by selecting "Start pomo with saved setting", then hitting the `e` key on the keyboard while the pomo to edit is selected.

<p align="center">
  <img src="./update.png" alt="Update">
</p>

## Delete a custom Pomo
After a pomo has been created, you can delete it by using `pomo -d <pomo_name>`, where "pomo_name" is the `name` value that you gave to your pomo. 

<p align="center">
  <img src="./delete.png" alt="Delete">
</p>

The delete pomo action can be accessed from the interactive menu by selecting "Start pomo with saved setting", then hitting the `d` key on the keyboard while the pomo to delete is selected. The user will be prompted if they are sure they want to delete the pomo before proceeding.

<p align="center">
  <img src="./deleteInteractive.png" alt="Delete">
</p>

## Start a pomo
To start your pomo, you can use the `pomo -p` command to simply start the previously used pomo. To start a specific pomo, type `pomo <pomo_name>`, where "pomo_name" is the `name` value that you gave to your pomo. 

This can be accessed from the interactive menu by selecting either "Start pomo with previous setting" or "Start pomo with saved setting", then hitting the `ENTER` key on the keyboard while the pomo to start is selected. 

When selected, the countdown timer will begin and it is time to focus!

<p align="center">
  <img src="./countdown.png" alt="Countdown">
</p>

During a Pomodoro session, the timer will count down to 00:00, signaling the end of the session. If breaks are enabled, they will start immediately afterward, followed by the next session.

## Fast Countdown
Pomo also features a very basic countdown timer. By entering `pomo <int>`, where `int` is any integer less than or equal to `99`, a countdown timer will begin from that number in minutes. For example, typing `pomo 25` will begin a simple countdown timer that will end after 25 minutes. Settings for the fast countdown mode can be found in the settings menu.

## Settings
Pomo has different customization options outside of the pomos that you create. In the settings tab, which is accessed by using `pomo -s` in the command line, or entering the "Enter settings" menu from the interactive menu, you will be able to change different settings.

<p align="center">
  <img src="./settings.png" alt="Settings">
</p>

You can use the `UP` and `DOWN` arrow keys to navigate between settings. Use the `ENTER` key to select which settings you want to change. Currently, you can change either "Main Menu Settings" or "Fast Countdown Settings"

### Main Menu Settings
Changing main menu settings will simply effect the main menu of the interactive interface. The customizations include changing the title of the ASCII art on the front (defaulted to display "POMO" on the screen) to any alpha characters with a max length of 6. Additionally, the user can change the border, time, and subtext color.

<p align="center">
  <img src="./mainMenuSettings.png" alt="Main Menu Settings">
</p>

### Fast Countdown Settings
These settings allow you to change the properties of the fast countdown. Similar to how we are able to customize our different pomos.

<p align="center">
  <img src="./fastCountdownSettings.png" alt="Fast Countdown Settings">
</p>