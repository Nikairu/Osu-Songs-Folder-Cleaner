# osu! Songs Folder Cleanup Script

This script is designed to help you clean up your osu! songs folder by deleting specific osu! beatmap related files. It provides options to delete different file types and different game modes and utilizes multithreading for efficient processing.

## Prerequisites

- Python 3.x
- tqdm package (`pip install tqdm`)

## Instructions

1. Clone or download the script to your local machine.
2. Install the required dependencies by running the following command:```pip install tqdm```
3. Open a terminal or command prompt and navigate to the directory where the script is located.
4. Run the script by executing the following command: ```python script.py```
5. Enter the full path to the 'osu!\Songs' folder when prompted.
6. Select your options from the deletion menu by entering the corresponding number.
7. Wait for the script to process the files. The progress will be displayed.

**Note**: The script uses multithreading to improve performance during file processing. It automatically determines the optimal number of threads based on your system's CPU count. 

For optimal performance, it is recommended to close unnecessary applications or processes running on your computer before running the script. This will free up system resources and allow the script to run more efficiently.

## File Type Options

1. Beatmaps: Deletes `.osu` files. You will be asked which beatmap modes you want to delete.
2. Video files: Deletes video files (`.mp4`, `.avi`, `.flv`) immediately and permanently.
3. Exit - Exit the program.

## Deletion Options

1. Delete files of all modes except Osu!Standard.
2. Delete only Standard mode files.
3. Delete only Taiko mode files.
4. Delete only Catch mode files.
5. Delete only Mania mode files.
6. Exit - Exit the program.
