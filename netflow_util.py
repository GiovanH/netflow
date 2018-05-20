#!/bin/python3
#Seth Giovanetti

import pickle
import os

def combine_data(data, equals, sortField):
    #Combines records in data based on the equals function.
    #Only sequential entries after sorting by sortfield will be combined.
    data_sorted = sorted(data, key=lambda k: k[sortField])
    p = data_sorted.pop()
    groups = []
    group = [p]
    group_sort = p
    while len(data_sorted) is not 0:
        p = data_sorted.pop()
        try:
            if (equals(group_sort, p)):
                group.append(p)
            else:
                groups.append(group)
                group = [p]
                group_sort = p
        except TypeError:
            print("Group_sort:")
            print(group_sort)
            print("New pop:")
            print(p)
            raise
    groups.append(group)
    finaldata = []
    for l in groups:
            combined = {}
            for key in l[0].keys():
                    value = 0
                    for entry in l:
                            try:
                                    value += entry[key]
                            except TypeError:
                                    value = entry[key]
                                    break
                    combined[key] = value
            finaldata.append(combined)
    return finaldata

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
