# Etrian Odyssey Untold Grimoire Editor

## Running
### Windows
Run the `eou_grimoire_editor.exe` file from the `dist/` folder. Make sure that the `skill_data/` folder is in the same directory as the executable file, otherwise it will not run.

### Mac/Linux
Requirements:
- Python 3 (with tkinter)
- Basic command line usage

Download the code from this repository navigate to the directory and using the terminal. From there, run the command below
```
python eou_grimoire_editor.py
```

You may need to install tkinter for Python3; this can be done on Ubuntu systems with the following command
```
sudo apt-get install python3-tk
```

## How to Use (with pictures!)

Obtain a backup of a save file for the game using `Checkpoint` or a similar tool for the 3DS. The file of interest should be called `mor1rgame.sav`. I strongly suggest backing up this save file in case things go wrong.

Launch the grimoire editor program and load the save file. You should see a screen similar to the one below on the left. I am going to change Raging Edge to Wolf Pack; once I begin typing Wolf Pack into the field it should auto-complete. Click `Enter` or `Return` and it should register the new skill. In addition, you can click `Up` or `Down` to cycle through the auto-complete options. If you want a level 10 Wolf Pack, you can use the dropdown to the side of the skill name and select the desired level, as I have done in the image on the right.

We can also edit the name of the character who generated the grimoire. A blank entry is Unknown origin; in this case I'm going to set the generator to be "Doot Do0t" as dummy text. Remember to hit `Enter` to register the changes. I'm also going to make the grimoire slightly damaged, even though it has a level 10 skill.

<div align="center">
<img src="img/eou_grim_1.jpg" alt="Change skill" width="80%"/>
</div>

You can select another grimoire from the menu on the left to edit multiple grimoires. I've selected the second grimoire in my inventory (the original can be seen on the left) to modify. I added the three gathering skills at level 5 as well as set the class to a spear, as shown on the right. Note that when changing a skill from "Blank," the level will automatically be set to 1. Since no name is specified for the generator, the grimoire will be of Unknown origin.

<div align="center">
<img src="img/eou_grim_2.jpg" alt="Gathering Grimoire" width="80%"/>
</div>

Once complete, use the `Save File` button to save the file with the modified grimoires. After loading the save file, we see the two grimoires in-game below. 

<div align="center">
<img src="img/grimoires_ingame.jpg" alt="in-game" width="80%"/>
</div>

Finally, as a sanity check the terminal window has a record of the changes made. Note that I forgot to click `Enter` when setting Mine in the second slot so the skill setting occurs after the level setting. The positions in the terminal align with their place on the in-game screen. This can be a good tool to verify when making edits to ensure that the changes register.

<div align="center">
<img src="img/eou_grim_terminal.PNG" alt="terminal output" width="80%"/>
</div>


## Build/Debug

Requirements:
- Python 3
- Pyinstaller

To run the program locally, please use the instructions to run on a Mac/Linux computer.

To build the `.exe` file locally, install [pyinstaller](https://pyinstaller.org/en/stable/) and run the following command
```
pyinstaller.exe --onefile eou_grimoire_editor.py
```
This will generate an executable file in the `dist/` directory (`eou_grimoire_editor.exe`). Make sure that the `skill_data/` folder is in the same directory as the executable file, otherwise it will not run.