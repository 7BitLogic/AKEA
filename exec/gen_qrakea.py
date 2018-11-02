# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 21:09:20 2017

Always use the first 42 bytes of the SHA512 digest.
For one it is faster then the SHA256 and second you can allways "upgrade"
to full 512 bit key without loss of compatibility for old keys!

@author: Raoul-Amadeus Lorbeer
"""
import os          #get the filename separated
import configparser
import sys

from win32api import SetFileAttributes
from win32con import FILE_ATTRIBUTE_READONLY

sys.path.append("..")
from akea import akea, qrakea

##_________________________________________________________##

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('akea.conf')

    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    #read a file:
    file_path = ''#"E:\\Programmieren\\AKEA\\depricated\\DBASH\\test\\test0011.bmp"

    to_print = 0    #don't print if necessarry
    do_folder = 0   #check if it is a whole folder

    if len(sys.argv) > 1:     #go through arguments passed to script
        command_list = enumerate(sys.argv[1:])
        for command in command_list:            #all but first argument
            if str(command).find('-') < 0:        #this should be the file!
                file_path = str(command)
                #make the file read only since we do not intend to modify them any more!
                SetFileAttributes(file_path, FILE_ATTRIBUTE_READONLY)
                data = akea.hex_digest(file_path)    #data = akea_digest(file_path)
                print(data)
                img = qrakea.generate_qr_code(data)
                img.save(file_path+'.qrakea', format='PNG', dpi=(600, 600))
                img.show()
            if str(command).find('-print') >= 0:  #to screen or to printer?
                file_path = str(next(command_list)[1])
                #make the file read only since we do not intend to modify them any more!
                SetFileAttributes(file_path, FILE_ATTRIBUTE_READONLY)
                data = akea.hex_digest(file_path)    #data = akea_digest(file_path)
                img = qrakea.generate_qr_code(data)
                img.save(file_path+'.qrakea', format='PNG', dpi=(600, 600))
                os.startfile(file_path + '.qrakea', 'print')
                #system(r'"C:\Program Files\IrfanView\i_view64.exe" ' + file_path + r'.png /print')
