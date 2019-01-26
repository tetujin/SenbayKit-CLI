# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name='SenbayKit',
    version='0.1.2',
    description='SenbayKit for Python',
    long_description='',
    author='Yuuki Nishiyama',
    author_email='yuuki.nishiyama@oulu.fi',
    url='https://github.com/tetujin/SenbayKit-CLI',
    license='Apache License 2.0',
    install_requires=['numpy','opencv-python','fastzbarlight','qrcode','mss','six'],
    packages=[
        'senbay'
    ],
)
