Steam Deck Ubisoft Rockstar and EA Launcher Deduplication Script

This script searches through game prefix folders on the Steam Deck to identify installed launchers from Ubisoft, Rockstar, and EA. It consolidates these launchers into a shared folder, removes duplicate copies within each prefix, and creates a shortcut to the shared folder in each prefix.

Benefits:

Increased Disk Space: By consolidating multiple launcher copies into one, you save valuable storage space.

Unified Updates: Launchers are updated only once, allowing multiple games from the same publisher to use the same, up-to-date version.

Centralized Settings Management: Configure launcher settings in one location rather than multiple instances across prefixes.

Automatic Login Functionality: Seamlessly log into all games using the shared launcher.

Changelog for v1.2

Installer
Allows for easy installation and updating of the script and automatically creates a desktop shortcut for quicker access to the tool.

Disk Space Check
At the start, the script checks if there’s at least 1GB of free space and exits if there’s not enough. At the end of the operation, it displays the current amount of free space.

Automatic Backup of Ubisoft Game Saves
In case of conflicts, game saves are automatically archived in the Launchers/Ubisoft savegames backup folder to ensure data integrity.

Deduplication Counter
The script reports the number of deduplicated launchers, giving users full insight into the process.

Improved Readability in Terminal
Output formatting has been enhanced, making the script's messages clearer and easier to follow.

Changelog for v1.1

Multi-use Capability
The script now supports multiple uses by skipping launcher folders that already have symlinks in place. This prevents redundant operations and speeds up processing. Please be advised, version 1.0 was one use only.

Automatic Copying and Merging of Save Games
Automatically copies and merges save games from different prefixes for the Ubisoft launcher. All saves are consolidated into a single shared folder for easy access.

Save Game Size Check
The script checks the size of Ubisoft launcher save games before copying to avoid accidentally overwriting different versions in the shared folder, ensuring data preservation and integrity.

Install instructions for v1.2:

[For freshly downloaded games, make sure to LAUNCH THEM AT LEAST ONCE to allow all necessary Proton files to be installed before running the script]

1. Go to the Steam Deck desktop.

2. Download the LD_archive.tar.gz and extract it.

3. Right click on install.sh and choose Run in Konsole.
(If installer is not working for you:
Open terminal
cd /home/deck/Downloads/LD/   (or other location you saved it)
chmod +x install.sh
Close terminal and go back to 3.)

4. Open Launcher Deduplication from desktop and follow instructions.
