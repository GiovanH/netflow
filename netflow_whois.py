#!/bin/python3

import jfileutil as j
import ipwhois
import pprint
import warnings

whoisData = {}
cachefilename = "whoiscache"

# Suppress ipwhois depreciation warnings. This is an issue with the core library and should be updated soon.

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)


def loadWhois():
    global whoisData  # Necessary to modifiy whoisData
    try:
        whoisData = j.load(cachefilename)
        print("Loaded whois cache with " + str(len(whoisData)) + " entries")
    except FileNotFoundError:
        print("Warning! Whois database not found. It will be rebuilt as needed.")
        # pass # We will build whoisdata ourselves and save it anyway.


def saveWhois():
    j.save(whoisData, cachefilename)


def populateDatabase(addresses, verbose=False, force=False):
    global whoisData  # Necessary to modifiy whoisData
    if whoisData == {}:
        loadWhois()
    for ip in addresses:
        print(ip)
        try:
            # Validate cached data.
            ipdata = whoisData[ip]
            if not (force is False and
                    ipdata.get('good') is True and
                    ipdata.get('version') == 1.0 and
                    ipdata.get('owner') is not None):
                raise KeyError('Data does not meet standards')
        except KeyError:
            whoisData[ip] = {}
            whoisData[ip]['version'] = 1.0
            whoisData[ip]['good'] = True
            try:
                ipdata = ipwhois.IPWhois(ip).lookup_rdap(depth=0)
                print("WHOIS: Acquired new data for ip " + ip)
                if verbose:
                    pprint.pprint(ipdata)
                whoisData[ip]['owner'] = ipdata['asn_description']
            except ipwhois.exceptions.IPDefinedError:
                whoisData[ip]['owner'] = "INTERNAL"
            except ipwhois.exceptions.HTTPLookupError:
                whoisData[ip]['owner'] = "UNKNOWN"
                whoisData[ip]['good'] = False
                print("Error looking up IP address " + ip)
    saveWhois()


def getOwnerPairing(addresses):
    populateDatabase(addresses)
    return {ip: whoisData[ip]['owner'] for ip in addresses}


def appendOwnerData(data, iptype):
    populateDatabase([entry[iptype] for entry in data])
    for entry in data:
        entry['whois_owner_' + iptype] = whoisData[entry[iptype]]['owner']


def getDetailedInformation(addresses, force=True, verbose=True):
    populateDatabase(addresses, force=force, verbose=verbose)
    pairing = getOwnerPairing(addresses)
    print(
        '\n'.join(
            [ip + "\t" + pairing[ip] for ip in addresses]
        )
    )


"""
import netflow_whois as whois
whois.getDetailedInformation(['4.4.4.4'],force=True,verbose=True)
"""
