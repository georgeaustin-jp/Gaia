# Gaia

*v0.1.2-alpha*

*See `patch_notes.md` for additional information about this version*

## Description

Gaia is a turn-based combat game, taking inspiration from Terraria, Pokémon and a large variety of other games. It is designed to run well on almost any computer, no matter how low-power it may be.

## Installation guide

Download and uncompress the latest release from the **Releases** section.

If you are on windows, enter the new folder, select the folder inside and right-click; it should have the same name as the folder you are currently in. Under the menu shown by the right-click, select the option to `open in terminal`. A powershell window with the following text should appear:

```shell
PS C:\...\Gaia-0.1.2-alpha\Gaia-0.1.2-alpha>
```

where the `...` is the path to the place where you have saved the project.

Then, to begin playing the game, enter the following text into the command line:

```shell
python src/main.py
```

## How to play

Equip up to 3 weapons and 4 equipables before entering combat. Weapons deal damage and can parry. Equipables increase your damage resistance by up to 5% each.

For each round of combat, you can select 2 actions out of the following:
 1. Attack an enemy
 2. Parry attacks
 3. Heal

Once you have selected your actions, the enemies will select theirs. The actions of both sides will then be executed in sequence.

You win once all your enemies have been killed. If you are killed, then you die and return home.

## Reporting bugs

If you encounter any errors in the program, please switch to the **Issues** tab of this repository.
