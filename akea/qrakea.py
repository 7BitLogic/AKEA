# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 21:09:20 2017

Always use the first 42 bytes of the SHA512 digest.
For one it is faster then the SHA256 and second you can allways "upgrade"
to full 512 bit key without loss of compatibility for old keys!

@author: Raoul-Amadeus Lorbeer
"""
#https://pypi.python.org/pypi/qrcode

from os import path#, system           #get the filename separated

import textwrap
import binascii
import qrcode       #convert to an image

from pyzbar.pyzbar import decode
import cv2
#import binascii
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#import configparser

def generate_qr_code(data):
    """Generate a QR code from given data.

    Generate a QR code from given data.

    Args:
        akea_digest (named tuple): digested tuple of data containing
                                    (path (str containing the original path),
                                    type (str identifying the AKEA spec),
                                    AKEA digest (AKEA HASH in binary)) compare akea_digest
    Returns:
        img (PIL image object): containing QR code
    """
    #some initial values
    border_width = 160 #px
    qr_box_size = 10
    qr_border = border_width/qr_box_size

    #qr setup
    qr_obj = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=qr_box_size,
        border=qr_border,
    )

    #Add data to QR code
    qr_obj.add_data(path.basename(data.path))
    if path.basename(data.path) == '':
        qr_obj.add_data(data.path)
    qr_obj.add_data(data.type)
    qr_obj.add_data(data.digest)
    qr_obj.make(fit=True)

    img = qr_obj.make_image()

    #refurbish borders
    # The crop rectangle, as a (left, upper, right, lower)-tuple.
    img = img.crop((qr_box_size*(qr_border-4), qr_box_size*(qr_border-4), \
                    img.size[0]-qr_box_size*(qr_border-4), img.size[1]))

    text = data.path
    if (len(data.digest[0]) > 1) & (len(data.digest) >= 50):
        text += '\n Warning! Some files may have been skipped!'

    __add_text_to_img(img, text, offset=(qr_box_size*4, img.size[1] - border_width))

    return img

def __add_text_to_img(img, qr_text, offset):
    """Draw text into image.

    Draw text into image at given offset position.

    Args:
        img (PIL image object): image object containing image
        qr_text (str): text
        offset (tuple): position of text insertion

    Returns:
        img (PIL image object): image object containing image with text
    """

    draw = ImageDraw.Draw(img)
    textsize = 24
    text_font = ImageFont.truetype("pix12pt.ttf", size=textsize)

    #@todo: I have no idea why it is not 2*offset[0]
    file_lines = textwrap.wrap(qr_text, width=int(((img.size[0]-2.75*offset[0])/(textsize))))
    wraped_file_name = ''

    for line in file_lines:
        wraped_file_name += line
        wraped_file_name += '\n'

    #prevent crash on empty last line https://github.com/python-pillow/Pillow/issues/2614
    wraped_file_name = wraped_file_name[:-1]

    #@toto: make font work again!   , font = text_font)
    draw.multiline_text(offset, wraped_file_name, fill='black', font=text_font)

    return img

def get_qr_webcam(config):   #https://pypi.python.org/pypi/pyzbar/
    """Collect QR code from Web-cam.

    Collect QR code from Web-cam.

    Args:
        config (configuration dictionary): setup information

    Returns:
        QRAKEA (binary): QRAKEA hash
    """
    qr_data = ''

    #start with vide capture dev 0 (standard web-cam)
    cap = cv2.VideoCapture(int(config['QRAKEA']['device_number']))

    #Set image dimensions
    cap.set(5, int(config['QRAKEA']['fps']))
    cap.set(3, int(config['QRAKEA']['x_res']))
    cap.set(4, int(config['QRAKEA']['y_res']))

    while True:
        # get frame
        return_val, frame = cap.read()

        # convert image data for pyzbar
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pil_object = Image.fromarray(img_gray)
        image = decode(pil_object)

        # display the resulting frame (convenience) and mirror (flip) makes it easier to place
        cv2.imshow('Please show the QRAKEA code to the camera. Hit space to exit.', cv2.flip(img_gray, 1))

        #extract results
        if len(image) > 0:
            qr_data = str(image[0].data)

        #abort scanning if enter was hit or QR-code was found
        if (cv2.waitKey(10) & 0xFF == ord(' ')) | (qr_data != ''):
            break        #nothing to scan!

    #clean up window
    cv2.destroyAllWindows()
    cap.release()

    #extract hex hash from QRcode-string
    hash_start = qr_data.rfind("_sha512-336x_")+13
    file_hash = qr_data[hash_start:-1]
    the_data = binascii.unhexlify(file_hash)

    return the_data

def get_qr_image(image_path):   #https://pypi.python.org/pypi/pyzbar/
    """Collect QR code from image.

    Collect QR code from image.

    Args:
        image_path (str): path to image

    Returns:
        QRAKEA (binary): QRAKEA hash
    """
    qr_data = ''
    #start with vide capture dev 0 (standard webcam)

    try:
        pil_object = Image.open(image_path)
    except OSError:# as e:
        #print("Could not open image.\n")
        return 0

    image = decode(pil_object)
    # extract results
    if len(image) > 0:
        qr_data = str(image[0].data)

    #extract hex hash from QRcode-string
    hash_start = qr_data.rfind("_sha512-336x_")+13	#need to create some meeningful variable to get rid of this hard coded 13

    if hash_start < 13:
        return 0            #no AKEA tag found

    file_hash = qr_data[hash_start:-1]
    the_data = binascii.unhexlify(file_hash)

    return the_data
