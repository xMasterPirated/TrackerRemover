# Clipboard URL Tracker Cleaner

A Windows program that runs in the background from the **System Tray** and automatically cleans URLs copied to the clipboard.

## What does it do?

The program detects changes in the clipboard. When it finds one or more URLs, it tries to remove known tracking parameters before placing the cleaned links back into the clipboard.

The list of tracking parameters it removes can be found in the: `trackers` file.

You can check or modify that list if you want to change which parameters are removed.

## Automatic startup

I recommend adding the executable to:

`Win + R` → `shell:startup`

This way, the program will start automatically with Windows and keep cleaning URLs while it is running.

## AI usage

AI was only used to create the **logo** and help write this **README**.

All the code, logic, and functionality of the program were made by me. xD
