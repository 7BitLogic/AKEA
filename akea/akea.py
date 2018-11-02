# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 21:09:20 2017

Always use the first 42 bytes of the SHA512 digest.
For one it is faster then the SHA256 and second you can always "upgrade" to full 512 bit key
without loss of compatibility for old keys!

@author: Raoul-Amadeus Lorbeer
"""
#https://pypi.python.org/pypi/qrcode
#https://docs.python.org/2/library/hashlib.html

import glob

#import copy
import collections  #use tuples in function returns without messing everything up!

import hashlib      #create some hashes

from os import path

def hex_digest(file_path):
    """Generate an AKEA hex digest

    Generate an AKEA hex digest as specified in the AKEA specification.

    Args:
        file_path (str): Path to specified file

    Returns:
        akea_digest (named tuple): digested tuple of data containing
        (path (str containing the original path),
        type (str identifying the AKEA spec), AKEA digest (AKEA HASH in hex))
    """
    #first check if we have a folder
    if path.isdir(file_path):         #no file only a folder
        akea = __hex_folder_digest(file_path)
    else:       #take first 42 bytes ->84 hex values of digest
        akea = hashlib.sha512(__get_file_data(file_path)).hexdigest()[0:84]
    return collections.namedtuple('akea_digest', ('path', 'type', 'digest')) \
                                        (file_path, '_sha512-336x_', akea)

def __hex_folder_digest(folder_path, max_files=50):
    """Generate an AKEA hex digest tuple

    Generate an AKEA hex digest tuple starting wit 42 byte and then continuing with
    4 byte segments as specified in the AKEA specification.

    Args:
        folder_path (str): Path to specified folder
        max_files (int): number of files which may be included in the hash tuple

    Returns:
        akea hex digest (tuple): digested tuple of data containing hex digests for
        up to 100 files in one folder
    """
    akea = []

    file_list = __non_qrakea_file_list(folder_path)

    if file_list == []:
        return akea

    #take first 42 bytes ->84 hex values of digest
    akea.append(hashlib.sha512(__get_file_data(file_list[0])).hexdigest()[0:84])

     #choose step size to assure <50 files to represent the whole set
    for file in file_list[:max(1,int((len(file_list)/max_files))):]:
        #take first 4 bytes ->8 hex values of digest
        akea.append(hashlib.sha512(__get_file_data(file)).hexdigest()[0:8])

    return akea

def binary_digest(file_path, max_files=100):
    """Generate an AKEA binary digest

    Generate an AKEA binary digest as specified in the AKEA specification.

    Args:
        file_path (str): Path to specified file
        max_files (int): number of files which may be included in the hash tuple

    Returns:
        akea_digest (named tuple): digested tuple of data containing
        (path (str containing the original path), type (str identifying the AKEA spec),
        AKEA digest (AKEA HASH in binary))
    """
    #first check if we have a folder
    if path.isdir(file_path):         #no file only a folder
        akea = __binary_folder_digest(file_path, max_files)
    else:       #take first 42 bytes of digest
        akea = hashlib.sha512(__get_file_data(file_path)).digest()[0:42]
    return collections.namedtuple('akea_digest', ('path', 'type', 'digest')) \
                                                (file_path, '_sha512-336_', akea)

def __binary_folder_digest(folder_path, max_files):
    """Generate an AKEA binary digest tuple

    Generate an AKEA binary digest tuple starting wit 42 byte and then continuing
    with 4 byte segments as specified in the AKEA specification.

    Args:
        folder_path (str): Path to specified folder
        max_files (int): number of files which may be included in the hash tuple

    Returns:
        akea binary digest (tuple): digested tuple of data containing hex digests
        for up to 100 files in one folder
    """
    akea = []

    file_list = __non_qrakea_file_list(folder_path)

    if file_list == []:
        return akea

    #take first 42 bytes
    akea.append(hashlib.sha512(__get_file_data(file_list[0])).digest()[0:42])

    #choose step size to assure <100 files to represent the whole set
    for file in file_list[:max(1,int((len(file_list)/max_files))):]:
        akea.append(hashlib.sha512(__get_file_data(file)).digest()[0:4])     #take first 4 bytes

    return akea

def __get_file_data(file_path):
    """Extract data from file

    Used to get all data included in the file at the specified path.

    Args:
        file_path (str): Path to specified file
        max_files (int): number of files which may be included in the hash tuple

    Returns:
        binary: data stored in specified file
    """

    file = open(file_path, 'rb')
    file_data = file.read()
    file.close()
    return file_data

def __non_qrakea_file_list(folder_path, subfolders=False):
    """Generate file list with or without sub-folders without "*.qrakea".

    Generate file list with or without sub-folders without "*.qrakea".

    Args:
        folder_path (str): path to be searched in

    Returns:
        filepath (list of str): paths to files aond folders in folder_path
    """
    if subfolders:
        file_list = [file for file in glob.glob(path.join(folder_path, r'**\*.*'), recursive=True)
                     if not path.splitext(file)[1] == '.qrakea']
    else:
        file_list = [file for file in glob.glob(path.join(folder_path, '*.*'))
                     if not path.splitext(file)[1] == '.qrakea']

    return file_list
