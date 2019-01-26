#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 06:17:17 2019

@author: Yuuki Nishiyama
"""

import sys
import time
import cv2

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
    width   = 640
    height  = 360
    fps     = 30 # fps
    threads = 10 # threading
    fourcc  = 'mp4v'
    camera_input_number = 0
    video_output_path   = None
    stdout  = False
    preview = True
    face    = False
    cascade = None
    cascade_path = "./cascade/haarcascade_frontalface_alt.xml"

    face_exist_status = 0

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
        if arg == "-f" or arg == "--face":
            cascade = cv2.CascadeClassifier(cascade_path)
            face = True
        if arg == "-c" or arg == "--video-codec":
            fourcc = args[i+1]

    def content_handler():
        sd = SenbayData();
        now = time.time()
        sd.add_number("TIME",now)
        if face is True:
            sd.add_number("FACE",face_exist_status)
        data = sd.encode();
        return data;

    def completion_handler():
        print("done");

    def frame_handler(frame):
        if face == True:
            facerect = cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
            print(facerect)
            color = (255, 255, 255)
            for rect in facerect:
                # croped =  frame[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
                # cv2.imwrite(str(time.time())+".jpg", croped)
                cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)

            if len(facerect) > 0:
                face_exist_status = 1
            else:
                face_exist_status = 0

        return frame;

    ### camera input
    camera = SenbayCamera(camera_number = camera_input_number,
                          video_output  = video_output_path,
                          width  = width,
                          height = height,
                          fps    = fps,
                          content_handler    = content_handler,
                          completion_handler = completion_handler,
                          frame_handler      = frame_handler,
                          stdout = stdout,
                          preview= preview,
                          fourcc = fourcc)

    print('You can quit this application by ESC button on the preview window.')

    camera.start()
