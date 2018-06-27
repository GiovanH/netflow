#!/bin/python3

import netflow_util as util
import ipwhois

whoisData = {}
cachefilename = "whoiscache"

#Suppress ipwhois depreciation warnings. This is an issue with the core library and should be updated soon.
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)


def loadWhois():
    global whoisData #Necessary to modifiy whoisData
    try:
        whoisData = util.pickleLoad(cachefilename)
        print("Loaded whois cache with " + str(len(whoisData)) + " entries")
    except FileNotFoundError:
        print("Warning! Whois database not found. It will be rebuilt as needed.")
        #pass # We will build whoisdata ourselves and save it anyway.

def saveWhois():
    util.pickleSave(whoisData, cachefilename)

def populateDatabase(addresses):
    print(addresses)
    global whoisData #Necessary to modifiy whoisData
    for ip in addresses:
        try:
            #Validate cached data.
            ipdata = whoisData[ip]
            assert ipdata.get('owner') is not None
            assert ipdata.get('owner') is not "UNKNOWN: LOOKUP FAILED???"
        except:
            try:
                ipdata = ipwhois.IPWhois(ip).lookup_rdap(depth=0)
                print("WHOIS: Acquired new data for ip " + ip)
                whoisData[ip] = {'owner': ipdata['asn_description']}
            except ipwhois.exceptions.IPDefinedError:
                whoisData[ip] = {'owner': "INTERNAL"}
            except ipwhois.exceptions.HTTPLookupError:
                whoisData[ip] = {'owner': "UNKNOWN: LOOKUP FAILED???"}
    saveWhois()
    
def getOwnerPairing(addresses):
    populateDatabase(addresses)
    return {ip: whoisData[ip]['owner'] for ip in addresses}

def appendOwnerData(data, iptype):
    populateDatabase([entry[iptype] for entry in data])
    for entry in data:
        entry['whois_owner'] = whoisData[entry[iptype]]['owner']
    
def selfTest():
    addresses = ['4.4.4.4','2.2.2.2']
    pairing = getOwnerPairing(addresses)
    print(
        '\n'.join(
            [ip + "\t" + pairing[ip] for ip in addresses]
        )
    )

loadWhois()
"""
import netflow_whois as whois
whois.getOwnerPairing(['4.4.4.4'])
"""