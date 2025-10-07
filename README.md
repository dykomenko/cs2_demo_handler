# CS2 Demo Handler

A lightweight Windows utility for Counter-Strike 2 replay files.

When you double-click a `.zst` or `.dem` file, this program automatically places the demo into your CS2 replay folder and copies the corresponding `playdemo` command to the clipboard.

---

## Features

- Extracts `.zst` files containing CS2 demos directly into the `game\csgo` folder.
- Copies `.dem` files without unpacking.
- Copies the `playdemo <demo_name>` command to clipboard automatically.
- Opens the CS2 demo folder on direct launch (without arguments).
- Reads CS2 installation path from a nearby configuration file.
- Includes `.bat` script for easy file association with `.zst` and `.dem`.

---

## Setup

1. Download the latest build from the [releases page](https://github.com/dykomenko/cs2_demo_handler/releases/latest).
2. Extract the archive to any folder.
3. Open the `cs2_path.txt` file and paste your Counter-Strike 2 installation path. The default path is already in the file.

