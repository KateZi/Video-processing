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
conda env create -f environment.yml
conda activate myenv
```

## Usage
The main script is "undistort-crop-concat"
```bash
python src/undistort-crop-concat # "Please choose the directory with videos"
```

For separate functionality use "Video_processing"
To run the script for:
1. Undistorting provide an argument "undistort"
2. Crop - "crop"
3. Concatenate - "concatenate"

## Example
```bash
python Video_processing crop # "Insert the directory to work in"
<directory with videos>
```
