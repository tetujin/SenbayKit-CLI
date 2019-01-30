#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 06:17:17 2017

@author: Yuuki Nishiyama
"""

import sys

import numpy as np
import cv2
import time
import qrcode
import six
from PIL import Image
from datetime import datetime

class SenbayFrame:
    qr_maker = None;
    fill_color = 'black';
    back_color = 'white';

    '''
    qr_box_size:
        A pixel size of error correct box.
        default value = 10

    qr_border:
        A border size of QR code.
        default value = 5

    qr_error_correction:
        qrcode.constants.ERROR_CORRECT_L(7%)
        qrcode.constants.ERROR_CORRECT_M(15%, default)
        qrcode.constants.ERROR_CORRECT_Q(25%)
        qrcode.constants.ERROR_CORRECT_H(30%)
    '''
    def __init__(self,
                 qr_box_size = 5,
                 qr_border   = 1,
                 qr_error_correction = qrcode.constants.ERROR_CORRECT_L,
                 qr_fill_color = 'black',
                 qr_back_color = 'white'):
        self.qr_maker = qrcode.QRCode(
                error_correction=qr_error_correction,
                box_size=qr_box_size,
                border=qr_border
                )
        self.fill_color = qr_fill_color
        self.back_color = qr_back_color

    def gen(self, frame=None, data=None):
        '''Generate a Senbay Frame based on the input video frame and data.

        Returns
        --------------
        senbay_frame : img
            An image of Senbay Frame.
        '''
        # Generate a QR code image
        self.qr_maker.add_data(data)
        self.qr_maker.make(fit=True)
        qrimg = self.qr_maker.make_image( fill_color=self.fill_color, back_color=self.back_color)
        self.qr_maker.clear()

        # Generate a QR code layer
        pil_image = qrimg.convert('RGB')
        qr_layer = np.array(pil_image)
        qr_layer = qr_layer[:, :, ::-1].copy()

        # Generate a base layer
        base_layer = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Put the QR code layer on the base layer
        return self.overlay(base_layer, qr_layer, 0, 0)


    def overlay(self, base_image, overlay_image, pos_x, pos_y):
        '''Compose two images using PIL.

        Parameters
        ----------
        base_image : img
            A base image.
        overlay_image : img
            A overlay image.
        pos_x : int
            A position (X-axis) of overlay image.
        pos_y : int
            A position (Y-axis) of overlay image.

        Returns
        ----------
        composed_image : img
            A composed image based on the parameters.
        '''
        # Get a size of the overlay image
        ol_height, ol_width = overlay_image.shape[:2]

        base_image_RGBA = base_image
        overlay_image_RGBA = overlay_image

        # Convert PIL from OpenCV image
        base_image_PIL=Image.fromarray(base_image_RGBA)
        overlay_image_PIL=Image.fromarray(overlay_image_RGBA)

        # Convert RGBA for composing
        base_image_PIL = base_image_PIL.convert('RGBA')
        overlay_image_PIL = overlay_image_PIL.convert('RGBA')

        # Generate a transparent image (the same size of the base image)
        tmp = Image.new('RGBA', base_image_PIL.size, (255, 255, 255, 0))
        # Put on the overlya image on the transparent image
        tmp.paste(overlay_image_PIL, (pos_x, pos_y), overlay_image_PIL)

        # Compose the base image and the transparent + overlay image
        result = Image.alpha_composite(base_image_PIL, tmp)

        # Convert COLOR_RGBA2BGRA to COLOR_RGBA2BGR for removing the alpha channel on the generated image. The alpha channel makes error for exporting a video file
        return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGR)

class SenbayCamera:
    width  = 640
    height = 360
    fps    = 30
    camera_number = None
    video_output  = None
    video_out     = None
    debug         = False

    ESC_KEY  = 27
    interval = 10

    preview  = True
    stdout   = False

    fourcc   = 'mp4v'

    content_handler      = None
    completion_handler   = None
    frame_handler        = None
    senbay_frame_handler = None
    senbay_frame_maker   = None

    def __init__(self,
                 camera_number=0,
                 video_output=None,
                 width=640, height=360, fps=30,
                 debug=False,
                 fourcc='mp4v',
                 preview=True,
                 stdout=False,
                 content_handler=None,
                 completion_handler=None,
                 frame_handler=None,
                 senbay_frame_handler=None,
                 senbay_frame_maker=None):
        self.camera_number = camera_number
        self.video_output =video_output
        self.height = height
        self.width = width
        self.fps = fps
        self.debug = debug
        self.preview = preview
        self.stdout = stdout
        self.content_handler = content_handler
        self.completion_handler = completion_handler
        self.frame_handler = frame_handler
        self.senbay_frame_handler = senbay_frame_handler
        self.fourcc = fourcc
        if senbay_frame_maker == None:
            self.senbay_frame_maker = SenbayFrame();
        else:
            self.senbay_frame_maker = senbay_frame_maker

    def start(self):
        '''Start SenbayCamera.
        '''

        camera_in = cv2.VideoCapture(self.camera_number)

        # http://www.fourcc.org/codecs.php
        fourcc = cv2.VideoWriter_fourcc(*self.fourcc)

        if self.video_output != None:
            video_out = cv2.VideoWriter(self.video_output, fourcc, self.fps,(self.width, self.height))


        while(camera_in.isOpened()):
            '''
            def content_handler(self):
                sd = SenbayData.SenbayData(121);
                now = time.time()
                sd.addNumber("TIME",now)
                data = sd.getSenbayFormattedData(True);
                return data;
            '''
            if self.content_handler != None:
                data = self.content_handler()
            else:
                data = ""

            # Capture frame-by-frame
            ret, frame = camera_in.read()
            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.flip(frame,1)
            if ret==False:
                break

            # handling frame
            if self.frame_handler != None:
                frame = self.frame_handler(frame)

            # generate a Senbay Frame
            senbay_frame = self.senbay_frame_maker.gen(frame=frame, data=data)

            # preview
            if self.preview == True:
                cv2.imshow('frame', senbay_frame)

            # video out put
            if self.video_output != None:
                video_out.write(senbay_frame)

            if self.senbay_frame_handler != None:
                self.senbay_frame_handler(senbay_frame)

            # stdout
            if self.stdout == True:
                if six.PY2:
                    sys.stdout.write( senbay_frame.tostring() )
                else:
                    sys.stdout.buffer.write( senbay_frame.tobytes() )

            key = cv2.waitKey(self.interval) & 0xFF
            if key is self.ESC_KEY:
                break

        # When everything done, release the capture
        camera_in.release()
        if self.video_output != None:
            video_out.release()
        cv2.destroyAllWindows()
        if self.completion_handler != None:
            self.completion_handler()
