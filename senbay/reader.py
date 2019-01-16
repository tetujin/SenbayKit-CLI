#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:54:04 2017

Senbay Reader

@author: Yuuki Nishiyama
"""

import sys

import numpy as np
import cv2
import fastzbarlight as zl
from PIL import Image
from mss import mss
from PIL import ImageGrab

# import core as sd
from senbay import SenbayData

class SenbayReader:

    reader_mode  = 0
    video_input  = None
    camera_input = 0
    preview_input = True
    mode = 0 # 0=video, 1=camera, 2=screen
    cap_area = {'top': 160, 'left': 160, 'width': 200, 'height': 200}
    sct = None;

    def __init__(self, mode=0, video_in=None, camera_in=0, cap_area=None, preview_in=True):
        self.reader_mode    = mode
        self.video_input    = video_in
        self.camera_input   = camera_in
        self.preview_input  = preview_in
        if cap_area != None:
            self.cap_area =  cap_area

    def set_capture_are(self, top=0, left=0, width=200, height=200):
        self.cap_area = {'top': top, 'left': left, 'width': width, 'height': height}

    def start(self, observer):
        if self.reader_mode == 0 or self.reader_mode == 'video':
            cap = cv2.VideoCapture(self.video_input)
            self.reader_mode = 0
        elif self.reader_mode == 1 or self.reader_mode == 'camera':
            cap = cv2.VideoCapture(self.camera_input)
            self.reader_mode = 1
        elif self.reader_mode == 2 or self.reader_mode == 'screen':
            self.reader_mode = 2
            sct = mss()
        else:
            print('error: The mode value should be take 0(=video), 1(=camera), or 2(=screen).')
            return


        codes = None
        senbayData = SenbayData()

        if self.reader_mode == 0 or self.reader_mode == 1:
            while(cap.isOpened()):

                ret, frame = cap.read()

                if ret==False:
                    continue
                    #break
                try:
                    normal = cv2.cvtColor(frame, 0)
                    cv2.imshow('frame',normal)

                    image = Image.fromarray(np.uint8(frame))

                    codes = zl.scan_codes('qrcode', image)
                    if codes != None and len(codes) > 0:
                        # print(codes[0].decode('utf-8'))
                        senbayDict = senbayData.decode(str(codes[0].decode('utf-8')))
                        observer(self, senbayDict);
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                except ValueError:
                    print("Error")

        elif self.reader_mode == 2:
            while True:
                # capture screen
                sct_img = sct.grab(self.cap_area)

                # generate an image
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                if self.preview_input:
                    cv2.imshow('frame', np.array(img))

                codes = zl.scan_codes('qrcode', img)
                if codes != None and len(codes) > 0:
                    # print(codes[0].decode('utf-8'))
                    senbayDict = senbayData.decode(str(codes[0].decode('utf-8')))
                    observer(self, senbayDict);

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

        cap.release()
        cv2.destroyAllWindows()
