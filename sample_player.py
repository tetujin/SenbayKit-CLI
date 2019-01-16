#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 06:17:17 2019

@author: Yuuki Nishiyama
"""

import sys
from senbay import SenbayReader

if __name__ == '__main__':

	'''
	$ ./sample_player.py ./media/video/sample.m4v
	'''

	if len(sys.argv[1:]) < 1:
		print('-----------------------------------------------------')
		print('[Error]   Please set a video file path as an argument')
		print('[Example] $ ./sample_player.py ./media/video/sample.m4v')
		print('-----------------------------------------------------')
	else:
		video_path = sys.argv[1];
		print(video_path)

		def showResult(self, data):
			print(data)

		reader = SenbayReader(video_in=video_path)
		reader.start(showResult)
