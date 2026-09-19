"""
testing ffmpeg_extract_subclip
"""
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

VIDPATH = ""  # TODO: set local path — folder containing the source session videos
input_fname = os.path.join(VIDPATH, 'P001_G_N.Camera1.mkv')
output_fname = ""  # TODO: set local path — output path for the test slice
test_start_seconds = 0
test_stop_seconds = 10
# open up a video, slice the video, write the videoest_stop = 0
ffmpeg_extract_subclip(input_fname, test_start_seconds, test_stop_seconds, targetname=output_fname)



