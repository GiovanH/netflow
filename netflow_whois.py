#!/bin/python3

import netflow_util as util
from ipwhois import IPWhois

whoisData = {}
cachefilename = "whoiscache"

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
    global whoisData #Necessary to modifiy whoisData
    for ip in addresses:
        try:
            ipdata = whoisData[ip]
        except:
            try:
                ipdata = IPWhois(ip).lookup_rdap(depth=0)
                print("WHOIS: Acquired new data for ip " + ip)
                whoisData[ip] = ipdata
            except ipwhois.exceptions.IPDefinedError:
                print("CRITICAL FAILURE: Cannot whois lookup an internal IP address!")
    saveWhois()
    
def getOwnerPairing(addresses):
    populateDatabase(addresses)
    return {ip: whoisData[ip]['asn_description'] for ip in addresses}
    
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