# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 21:09:20 2017

@author: Raoul-Amadeus Lorbeer
"""

import os           #get the filename separated

import sqlite3

from akea import akea
from akea import qrakea

#import configparser

def add_file_list(dbakea_cursor, dbakea, dirname, skip_sub_dirs=False):
    """append given file to AKEA database

    append given file to AKEA database.

    Args:
        dbakea_cursor (cursor object): cursor object to edit given database
        dbakea (database object): database object with opened file connection
        dirname (str): path to file or folder
        skip_sub_dirs (bool): subdirs are note added if true
    """
    print('Adding folder: ' + dirname)

    tag = 'none'
    version = 1.0
    file_list = []
    if os.path.isdir(dirname):
        file_list = akea.__non_qrakea_file_list(dirname, not skip_sub_dirs)
    else:
        file_list.append(dirname)

    #if skip_sub_dirs:
        #names = file_list#@todo: edit names to ommit subdirs!
        #return

    for file_name_i in file_list:    #add all files in list to database
        current_path = file_name_i      #obsolete?: os.path.join(dirname, file_name_i)
        try:
            data = akea.binary_digest(current_path)
            print(current_path)
            dbakea_cursor.execute("INSERT INTO files VALUES (?,?,'empty','empty',?,?)", \
                                      (current_path, memoryview(data.digest), tag, version))
        except sqlite3.Error:
            dbakea_cursor.execute('SELECT * FROM files WHERE AKEA=?', (memoryview(data.digest),))
            db_filepaths = dbakea_cursor.fetchone()[0]
            if db_filepaths.find(current_path) < 0:
                dbakea_cursor.execute('UPDATE files SET path = ? WHERE AKEA = ?', \
                                      ((db_filepaths + '; '+current_path), \
                                       memoryview(data.digest)))
            #else:
                #print("file known")
        except IOError:
            print("Could not access: " + current_path)
    dbakea.commit()

def append_to_db(path, config):
    """append given file to AKEA database

    append given file to AKEA database.

    Args:
        path (str): path to file or folder
        config (configuration parser = dictionary): system configuration
    """
    print(config['DBAKEA']['dbpath'])
    dbakea = sqlite3.connect(str(config['DBAKEA']['dbpath']))
    dbakea_cursor = dbakea.cursor()

    # Create table
    #check if table already exists!!
    try:
        dbakea_cursor.execute('''CREATE TABLE files
        (path text, AKEA blob, parent text, child text, TAG text, Version real, PRIMARY KEY (AKEA))
        ''')
    except sqlite3.Error:
        print("Table found")

    add_file_list(dbakea_cursor, dbakea, path)


def check_qr(config, image_file=''):
    """Search for file with QR code.

    Search for file with QR code from web-cam.

    Args:
        config (configuration parser = dictionary): system configuration

    Returns:
        filepath (str): path to file
    """
    the_data = 0
    if image_file != '':
        the_data = qrakea.get_qr_image(image_file)

    if the_data == 0:
        the_data = qrakea.get_qr_webcam(config)

    #search database entry
    dbakea = sqlite3.connect(config['DBAKEA']['dbpath'])
    dbakea_cursor = dbakea.cursor()
    dbakea_cursor.execute('SELECT * FROM files WHERE AKEA=?', (memoryview(the_data),))

    #get path / link
    db_filepaths = dbakea_cursor.fetchone()[0]
    print(db_filepaths)

    #close all
    dbakea.close()

    return str(db_filepaths)