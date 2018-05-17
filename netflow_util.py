#!/bin/python3
#Seth Giovanetti

import pickle
import os

def pickleLoad(filename):
    """
    TODO: Docstring
    Description in english.

    Returns: Return type

    Parameters:
    parameter -- description
    """
    filehandler = open("obj/" + filename + ".obj", 'rb')
    object = pickle.load(filehandler)
    return object

def pickleSave(object, filename):
    """
    TODO: Docstring
    Description in english.

    Returns: Return type

    Parameters:
    parameter -- description
    """
    os.makedirs("obj/" + filename)
    filehandler = open("obj/" + filename + ".obj", 'wb')
    pickle.dump(object, filehandler)
