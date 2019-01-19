#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 06:17:17 2019

@author: Yuuki Nishiyama
"""

import sys
import time

from senbay import SenbayCamera
from senbay import SenbayData

if __name__ == '__main__':

    '''
    -w --width        640
    -h --height       360
    -o --video-output None
    -i --camera-input 0
    -r --fps          30
    '''
    width  = 640
    height = 360
    fps = 30 # fps
    threads = 10 # threading
    camera_input_number  = 0
    video_output_path = None
    stdout = False
    preview = True

    args = sys.argv
    for i in range(1, len(sys.argv)):
        arg = args[i]
        if arg == "-w" or arg == "--width":
            width = int(args[i+1])
        if arg == "-h" or arg == "--height":
            height = int(args[i+1])
        if arg == "-o" or arg == "--video-output":
            video_output_path = args[i+1]
        if arg == "-i" or arg == "--camera-input":
            camera_input_number = int(args[i+1])
        if arg == "-r" or arg == "--fps":
            fps = int(args[i+1])
        if arg == "-s" or arg == "--stdout":
            stdout = True
        if arg == "--without-preview":
            preview = False

    def content():
        sd = SenbayData();
        now = time.time()
        sd.add_number("TIME",now)
        data = sd.encode();
        return data;

    def completion():
        print("done")

    ### camera input
    camera = SenbayCamera(camera_number=camera_input_number,
                          video_output=video_output_path,
                          width=width,
                          height=height,
                          fps=fps,
                          content=content,
                          completion=completion,
                          stdout=stdout,
                          preview=preview)

    camera.start()

    print('You can quit this application by ESC button on the preview window.')
