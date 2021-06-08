# How to use
Run python script with one parameter. The parameter should be the watch presentation link BBB gave you.

Output will be a list of commands to enter in your terminal. If you run all those commands, the webcam recording will be downloaded (because it contains the audio), then the shapes.svg file will be downloaded which contains positions and URLs of the slides, then the slides will be downloaded, and a video file will be created for each slide. The slides will then be concatenated and merged with the audio, which is extracted, to a file called __final.mp4__.

Because of a bug in BBB which creates a wrong time for the last slide, you need to edit the last video creation command to use the right time. You need to figure out yourself how long the last slide should be displayed.

## Example usage
```bash
python3 main.py https://example.org/playback/presentation/2.3/123a4-123 > commands.sh
# now edit the third line from the bottom in commands.sh
# to make the -t parameter use the right length
# like ffmpeg -loop 1 -i image30.png -c:v libx264 -t 70 -pix_fmt yuv420p -r 15.000150 image30.mp4 
# where 70 means 70 seconds
bash commands.sh
```

# Notes

Note that while the files will be small, video will still be actually rendered, so the process needs quite a lot of computing power or time. For 70 minutes of recording it took me 10 minutes on a medium 2020 PC. If your internet connection is not fast, that time needs to be added, too.

BBB sources are roughly 2 MB / minute for the audio and webcam and 500 KB per slide (can vary depending on the amount of webcams displayed).

# Requirements
This script is meant to be run on Linux. The commands require ffmpeg and wget.

A text file will be written to the directory of this script as an input for the concetanation so this script needs to be placed in a writable directory.

# Source
https://github.com/Konzertheld/bbb-slides-video-python
