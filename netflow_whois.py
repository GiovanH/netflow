#!/bin/python3

import jfileutil as j
import ipwhois
import traceback

whoisData = {}
cachefilename = "whoiscache"

DATA_VERSION = 1.0


def loadWhois():
    global whoisData  # Necessary to modifiy whoisData
    try:
        whoisData = j.load(cachefilename)
        print("Loaded whois cache with " + str(len(whoisData)) + " entries")
    except FileNotFoundError:
        print("Warning! Whois database not found. It will be rebuilt as needed.")
        # pass # We will build whoisdata ourselves and save it anyway.


def saveWhois():
    print("WHOIS: Saving whois cache")
    j.save(whoisData, cachefilename)


def populateDatabase(addresses, verbose=True, force=False):
    global whoisData  # Necessary to modifiy whoisData
    if whoisData == {}:
        loadWhois()
    i = 0
    for ip in addresses:
        try:
            # Validate cached data.
            ipdata = whoisData.get('ip')
            if ipdata is None:
                raise KeyError("No cached data for IP " + ip)
            if not (force is False):
                raise KeyError('Forcing update')
            # if ipdata.get('good') is not True:
            #     raise KeyError(ip + ' Not Good')
            if ipdata.get('version') != DATA_VERSION:
                raise KeyError(ip + ' Outdated')
            if ipdata.get('owner') is None:
                raise KeyError(ip + ' No Owner')
        except KeyError as Error:
            if verbose: print(Error)
            whoisData[ip] = {}
            whoisData[ip]['version'] = DATA_VERSION
            whoisData[ip]['good'] = True
            try:
                ipdata = ipwhois.IPWhois(ip).lookup_rdap(depth=0)
                # Try to get an owner name from asn_description
                owner = ipdata.get('asn_description')
                if owner is None:
                    # If that doesn't work, try another field.
                    owner = ipdata.get('network').get('name')
                #If that still didn't work, we have a problem. 
                if owner is None:
                    if verbose: print("Can't get owner for IP " + ip + ", logging")
                    # Save error report
                    j.json_save(ipdata, "err/bad_ip/noowner_" + ip)
                    owner = "UNKNOWN"
                    # Mark record as bad
                    whoisData[ip]['good'] = False
                whoisData[ip]['owner'] = owner
                # print("WHOIS: Acquired new data for ip " + ip + " with owner " + owner)
            except ipwhois.exceptions.IPDefinedError:
                print("WHOIS: IP is a reserved internal address: " + ip)
                whoisData[ip]['owner'] = "INTERNAL"
            except ipwhois.exceptions.HTTPLookupError:
                whoisData[ip]['owner'] = "UNKNOWN"
                whoisData[ip]['good'] = False
                if verbose: print("WHOIS: Error looking up IP address " + ip)
                # Save error report
                j.json_save(traceback.format_exc(limit=2).split('\n'), "err/bad_ip/httplookup_" + ip)
            i += 1
            if i % 120 == 0:
                saveWhois()
    saveWhois()


def getOwnerPairing(addresses):
    populateDatabase(addresses)
    return {ip: whoisData[ip]['owner'] for ip in addresses}


def appendOwnerToData(data, iptype):
    populateDatabase([entry[iptype] for entry in data])
    for entry in data:
        entry['whois_owner_' + iptype] = whoisData[entry[iptype]]['owner']


def appendOwnersToData(data):
    populateDatabase([entry["dest_ip"] for entry in data] + [entry["src_ip"] for entry in data])
    for entry in data:
        for iptype in ["dest_ip", "src_ip"]:
            entry['whois_owner_' + iptype] = whoisData[entry[iptype]]['owner']


def appendOwnersToEntry(entry):
    for iptype in ["dest_ip", "src_ip"]:
        populateDatabase([entry[iptype]])
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
