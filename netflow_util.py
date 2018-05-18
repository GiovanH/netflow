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
    filehandler = open(path(filename), 'rb')
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
    print("Saving " + path(filename))
    try:
        os.makedirs(path(filename)[:path(filename).rindex('/')])
    except FileExistsError:
        pass
    filehandler = open(path(filename), 'wb')
    inst = pickle.Pickler(filehandler)
    inst.dump(object)
    inst.clear_memo()

def path(file):
    return "obj/" + file.replace(".","_").replace("\\","_") + ".obj"
