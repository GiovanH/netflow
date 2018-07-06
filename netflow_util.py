#!/bin/python3
#Seth Giovanetti

import pickle
import os

def simple_combine_data(data,sortField):
    return combine_data(data, lambda a,b: a[sortField]==b[sortField], sortField)

def combine_data(data, equals, sortField):
    #Combines records in data based on the equals function.
    #Only sequential entries after sorting by sortfield will be combined.
    if len(data) is 0:
        print("Warning! Data is empty!")
        return data
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

def top_percent(predata, percent, field, total):
    totalrecords = len(predata)
        
    #Get top 10 records by bytes_in
    #Sorts the list by field (bytes_in), gets the #n... #2, #1 entries.
    predata = sorted(predata, key=lambda k: k[field])
    
    #Initialize array for the final data points
    data = []
    #Map included/total ratio while adding
    included = 0
    
    #Calculate top % of data, and use that as the data we graph
    #Until the amount of data we have exceeds %[percent], move a data point into our final list.
    while len(predata) > 0 and included < total*(percent/100):
        newrecord = predata.pop()
        included += newrecord[field]
        data.append(newrecord)
    print("Records included: " + str(len(data)) + '/' + str(totalrecords))
    return data
    
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

def sluggify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    r = value.replace("..\\","prev")
    r = r.replace("\"","").replace(" ","_")
    r = r.replace("\\","_").replace("/","_")
    r = r.replace("*","+").replace("%","perc")
    return r