# Etrian Odyssey Untold Grimoire Editor

## Overview / How to use

Obtain a backup of a save file for the game using `Checkpoint` or a similar tool for the 3ds. 


## Running
### Windows
Run the `eou_grimoire_editor.exe` file from the `dist/` folder. Make sure that the `skill_data/` folder is in the same directory as the executable file, otherwise it will not run.

### Mac/Linux
Requirements:
- Python 3 (with tkinter)
- Basic command line usage

Download the code from this repository and using the terminal navigate to the directory. From there, run the command below
```
python eou_grimoire_editor.py
```


## Build/Debug

Requirements:
- Python 3
- Pyinstaller

To build the `.exe` file locally, install [pyinstaller](https://pyinstaller.org/en/stable/) and run the following command
```
pyinstaller.exe --onefile eou_grimoire_editor.py
```
This will generate an executable file in the `dist/` directory (`eou_grimoire_editor.exe`). Make sure that the `skill_data/` folder is in the same directory as the executable file, otherwise it will not run.