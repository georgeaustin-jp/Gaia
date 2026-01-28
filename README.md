# Gaia

*v1.0.1*

*See `patch_notes.md` for additional information about this version*

#### Contents:
 * [Description](#description)
 * [Installation guide](#installation-guide)
   * [Dependencies](#dependencies)
   * [Running](#running)
 * [How to play](#how-to-play)
 * [Information for testers](#information-for-testers)
   * [Response form](#response-form)
   * [Reporting bugs](#reporting-bugs)

## Description

Gaia is a turn-based combat game, taking inspiration from Terraria, Pokémon and a large variety of other games. It is designed to run well on almost any computer, no matter how low-power it may be.

## Installation guide

Download and uncompress the latest release from the **Releases** section.

If you are on Windows or Mac, enter the uncompressed folder in your file manager. If there are more folders, continue until you enter a directory containing multiple folders and files. Right-click here and select the option to `open in terminal`. A terminal window with something looking like the following text appearing (for Windows Powershell):

```powershell
PS C:\...\Gaia-1.0.1>
```

where the `...` is the path to the place where you have saved the project.

If you are using a non-Windows OS, please be aware that the GUI looks different for other platforms, so you may encounter some visual bugs.

### Dependencies

python >=3.11, !=3.14.1

poetry >=2.3.1

Python can simply be installed from the Python website.

Poetry manages all the other packages, imports and dependencies. I recommend using Pip to install it.

### Running

To begin playing the game, enter the following text into the command line:

```shell
poetry install
poetry run python src/main.py
```

## How to play

Equip up to 3 weapons and 4 equipables before entering combat. Weapons deal damage and can parry. Equipables increase your damage resistance by up to 5% each.

For each round of combat, you can select 2 actions out of the following:
 1. Attack an enemy
 2. Parry attacks
 3. Heal

Once you have selected your actions, the enemies will select theirs. The actions of both sides will then be executed in sequence.

You win once all your enemies have been killed. If you are killed, then you die and return home.

### Abilities

Each weapon's attack can have abilities which go alongside it. These are as follows:
 * Ignition (Ig): deals 3 damage per turn for 3 turns
 * Pierce (Pr): all damage resistances are ignored
 * Weaken (Wk): temporarily reduce damage resistance of target
 * Parry (Pa): block up to a certain threshold of damage, with a percentage of the damage blocked being sent back to attacking enemies
 * Defend (Df): increase damage resistance

## Information for testers

If you are reading this with the intent of testing, I would first like to thank you for your time. Make sure you fill out the Google Form

### Response form

Once you feel like you have played the game enough, please fill out [this Google Form](https://docs.google.com/forms/d/e/1FAIpQLScbxpg9gDIR3d_emqDVAaNEb-gyg2ng785NHnq2XErT7M_3xg/viewform?usp=header). It has a section for general feedback, as well as for any feedback on bugs and errors. I will be more likely to respond about errors if you report it on this repository (see [Reporting bugs](#reporting-bugs)), but having bug reports on the Form will be greatly appreciated regardless.

If you have any issues with using the Google Form, as I have heard others in the past have, feel free to contact me.

### Reporting bugs

If you encounter any errors in the program, please switch to the **Issues** tab of this repository. Click the `Create new issue` button, after which you will be greeted with the following screen:

<img width="1312" height="882" alt="image" src="https://github.com/user-attachments/assets/8d65dfc9-a69d-4f60-8e57-cf19277f6bcc" />

When adding information about the error, please try and add:
 * Description about the error that happened
 * What you were doing before the error occured
 * Any error messages in the terminal

Include screenshots if possible. Also, try to add the version of the game which you were running. This is not necessary if you have a full screenshot of the game window, as the version of the game will be displayed in the window title.


