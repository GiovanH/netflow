#!/bin/python3

import netflow_util as util
import ipwhois
import pprint
import traceback
import warnings

whoisData = {}
cachefilename = "whoiscache"

# Suppress ipwhois depreciation warnings. This is an issue with the core library and should be updated soon.

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)


def loadWhois():
    global whoisData  # Necessary to modifiy whoisData
    try:
        whoisData = util.pickleLoad(cachefilename)
        print("Loaded whois cache with " + str(len(whoisData)) + " entries")
    except FileNotFoundError:
        print("Warning! Whois database not found. It will be rebuilt as needed.")
        # pass # We will build whoisdata ourselves and save it anyway.


def saveWhois():
    util.pickleSave(whoisData, cachefilename)


def populateDatabase(addresses, verbose=False, force=False):
    global whoisData  # Necessary to modifiy whoisData
    if whoisData == {}:
        loadWhois()
    for ip in addresses:
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
                # print(traceback.format_exc())
            except ipwhois.exceptions.HTTPLookupError:
                # print(traceback.format_exc())
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
