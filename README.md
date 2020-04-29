# Video-resizing
This is a small project in Python providing functionality for undistorting, cropping and concatenating videos using OpenCV.

## Installation
```bash
git clone https://github.com/KateZi/Video-processing.git
cd Video-processing
```
I suggest using [Anaconda](https://www.anaconda.com) to create an environemnt for running the script.
Once Anaconda is installed:
```bash
conda create --name <env_name> --file requirements.txt
conda activate <env_name>
```

## Usage
The main script is "Video_processing"
To run the script for:
1. Undistorting provide an argument "undistort"
2. Crop - "crop"
3. Concatenate - "concatenate"

## Usage Example
```bash
python Video_processing crop # "Insert the directory to work in"
<directory with videos>
```
