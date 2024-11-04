#!/usr/bin/env python3

import os
import shutil
from datetime import datetime

# Define paths and folders
launchers_dir = "/home/deck/.local/share/Steam/steamapps/compatdata/Launchers"
prefixes_root = "/home/deck/.local/share/Steam/steamapps/compatdata"
folders_to_find = [
    "Program Files (x86)/Ubisoft",
    "Program Files/Rockstar Games",
    "Program Files/Electronic Arts"
]
savegames_relative_path = "Program Files (x86)/Ubisoft/Ubisoft Game Launcher/savegames"

# Ensure the Launchers directory exists
os.makedirs(launchers_dir, exist_ok=True)

# Counter for processed folders
processed_count = 0

# Helper function for printing in red bold text
def print_bold_red(text):
    print(f"\033[1m\033[91m{text}\033[0m")

# Helper function for printing in blue bold text
def print_bold_blue(text):
    print(f"\033[1m\033[94m{text}\033[0m")

# Helper function for printing in bold text without color
def print_bold(text):
    print(f"\033[1m{text}\033[0m")

# Helper function for printing normal text with bold "skipping"
def print_normal_with_bold_skipping(text):
    print(f"{text}, \033[1mskipping\033[0m")

# Initial message
print_bold_blue("Steam Deck Ubisoft, Rockstar and EA Launcher Deduplication Script v1.1")
print("Script consolidates launcher installations, removes duplicates and ensures Ubisoft savegames are preserved without conflicts.")
print(" ")
print_bold_red("For freshly downloaded games, make sure to LAUNCH THEM AT LEAST ONCE to allow all necessary Proton files to be installed before running the script.")
print(" ")

# Disk space check function (1 GB minimum requirement)
def check_disk_space():
    total, used, free = shutil.disk_usage("/home")
    free_gb = free / (2**30)  # Convert to GB with decimals for accuracy
    print(f"Available disk space: {free_gb:.2f} GB.")  # Display with two decimal places
    return free_gb

# Save info about free disk space
initial_free_space = check_disk_space()

# Check disk space before proceeding
if initial_free_space < 1:  # Assuming 1 GB minimum space required
    print_bold_red("Not enough free disk space. Shutting down.")
    exit()

# Initial message
print("Press any key to continue...")
input()  # Wait for user to press any key to continue

# Function to handle savegames with conflict check and conditional backup creation
def copy_savegames_with_conflict_check(src, dest):
    backup_dir_created = False  # Track if backup folder is created

    if src.startswith(launchers_dir):
        print_normal_with_bold_skipping(f"Launchers folder is not a source {src}")
        return
    
    for root, _, files in os.walk(src):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src)
            dest_file = os.path.join(dest, rel_path)
            
            if os.path.abspath(src_file) == os.path.abspath(dest_file):
                print_normal_with_bold_skipping(f"Skipping copy for {src_file} as source and destination are the same")
                continue
            
            if os.path.exists(dest_file):
                # Check for conflict by comparing file sizes
                if os.path.getsize(src_file) != os.path.getsize(dest_file):
                    # Create the backup folder only once when a conflict is detected
                    if not backup_dir_created:
                        backup_dir = os.path.join(launchers_dir, "Ubisoft savegames backup")
                        os.makedirs(backup_dir, exist_ok=True)
                        backup_dir_created = True  # Set flag to avoid re-creating the folder
                    
                    # Maintain the subfolder structure within the backup directory
                    backup_file_path = os.path.join(backup_dir, rel_path)
                    os.makedirs(os.path.dirname(backup_file_path), exist_ok=True)
                    shutil.copy2(dest_file, backup_file_path)
                    print_bold_red(f"Savegame file conflict detected. Backup created at {backup_file_path}")
            
            # Copy file if no conflict or after creating a backup
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(src_file, dest_file)
            print_bold(f"Copied savegame file {src_file} to {dest_file}")

# Function to handle a single launcher folder in a prefix
def process_folder(prefix_path, relative_folder):
    global processed_count
    original_folder = os.path.join(prefix_path, "pfx/drive_c", relative_folder)
    launcher_folder = os.path.join(launchers_dir, os.path.basename(relative_folder))
    
    # Check if original_folder is a symlink already pointing to the launcher_folder
    if os.path.islink(original_folder) and os.readlink(original_folder) == launcher_folder:
        print_normal_with_bold_skipping(f"Symlink already exists for {original_folder}")
        return

    if os.path.exists(original_folder):
        if not os.path.exists(launcher_folder):
            # First occurrence: Copy folder to Launchers and create symlink
            shutil.copytree(original_folder, launcher_folder)
            print_bold(f"Copied {original_folder} to {launcher_folder}")
        # Remove the original and replace with symlink
        shutil.rmtree(original_folder)
        os.symlink(launcher_folder, original_folder)
        print_bold(f"Replaced {original_folder} with symlink to {launcher_folder}")
        processed_count += 1  # Increment counter

# Traverse each prefix and process the folders
for prefix in os.listdir(prefixes_root):
    prefix_path = os.path.join(prefixes_root, prefix)
    if os.path.isdir(prefix_path):
        # Skip processing if the prefix path is the Launchers folder
        if prefix_path == launchers_dir:
            print_normal_with_bold_skipping(f"Launchers folder is not a source {launchers_dir}")
            continue

        # Check if Ubisoft is a symlink and skip savegames processing if true
        ubisoft_path = os.path.join(prefix_path, "pfx/drive_c", "Program Files (x86)/Ubisoft")
        if os.path.islink(ubisoft_path):
            print_normal_with_bold_skipping(f"Symlink already exists for {ubisoft_path}")
            continue

        # Check and handle savegames folder separately for Ubisoft
        savegames_folder = os.path.join(prefix_path, "pfx/drive_c", savegames_relative_path)
        target_savegames_folder = os.path.join(launchers_dir, "Ubisoft/Ubisoft Game Launcher/savegames")
        
        if os.path.exists(savegames_folder):
            print_bold(f"Processing savegames from {savegames_folder}")
            copy_savegames_with_conflict_check(savegames_folder, target_savegames_folder)

        # Process main folders (Ubisoft, Rockstar, EA)
        for folder in folders_to_find:
            process_folder(prefix_path, folder)

# Display counter
print(" ")
print_bold_blue(f"Processing complete. Total launchers deduplicated: {processed_count}")

# Check disk space
final_free_space = check_disk_space()

# Display final message with GitHub link
print("You can find Launchers in /home/deck/.local/share/Steam/steamapps/compatdata/Launchers/")
print(" ")
print_bold_blue("Follow for new updates of this script: https://github.com/F3edo/Steam-Deck-Ubisoft-Rockstar-and-EA-Launcher-Deduplication-Script-for-Steam-Prefixes")
print(" ")
