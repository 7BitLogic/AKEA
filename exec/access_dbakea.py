# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 21:09:20 2017

Always use the first 42 bytes of the SHA512 digest.
For one it is faster then the SHA256 and second you can allways "upgrade"
to full 512 bit key without loss of compatibility for old keys!

@author: Raoul-Amadeus Lorbeer
"""
import configparser
import os           #get the filename separated
import sys
sys.path.append("..")
from akea import dbakea

def get_path(config, the_image):
       #open file
    try:  #if there is a file path attached to the command
        return dbakea.check_qr(config, the_image)
    except StopIteration:  #if not do it old school
        return dbakea.check_qr(config)

##Script starts here
##_________________________________________________________##

if __name__ == '__main__':

    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    #read a file:
    #file_path = 'E:\Programmieren\QR\DBakea\\testB\\'

    config = configparser.ConfigParser()
    config.read('akea.conf')

    if len(sys.argv) > 1:     #go through arguments passed to script
        command_list = enumerate(sys.argv[1:])
        for command in command_list:
            if str(command).find('-') < 0:
                dbakea.append_to_db(command, config)
                break
            if str(command).find('-pathqr') >= 0:
                #open folder
                os.startfile("\"" + os.path.dirname(str.split(get_path(config, \
                                 next(command_list)[1]), ';')[0]) + "\"")
                break
            if str(command).find('-openqr') >= 0:
                #open file
                os.startfile("\"" + os.path.abspath(str.split(get_path(config, \
                                 next(command_list)[1]), ';')[0]) + "\"")
                break
