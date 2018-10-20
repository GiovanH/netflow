#!/bin/python3

import jfileutil as j
import ipwhois
import traceback
import netflow_db
import progressbar

DATA_VERSION = 2.0
UNKNOWN = "UNKNOWN"
INTERNAL = "INTERNAL"


def whoisOwner(db, ip, verbose=False):
    if type(ip) is bytes:
        ip = ip.decode()
    name = db.getOwner(ip)
    if name is not None:
        return name
    else:
        if verbose:
            print("Cache miss: {0}".format(ip))
        try:
            ipdata = ipwhois.IPWhois(ip).lookup_rdap(depth=0)
            # Try to get an owner name from asn_description
            owner = ipdata.get('asn_description')
            if owner is None:
                # If that doesn't work, try another field.
                owner = ipdata.get('network').get('name')
            # If that still didn't work, we have a problem.
            if owner is None:
                if verbose:
                    print("Can't get owner for IP {0}, logging".format(ip))
                # Save error report
                j.json_save(ipdata, "err/bad_ip/noowner_{0}".format(ip))
                owner = UNKNOWN
            return db.pushPair(ip, owner)
        except ipwhois.exceptions.IPDefinedError:
            print("WHOIS: IP is a reserved internal address: " + ip)
            return db.pushPair(ip, INTERNAL)
        except (ipwhois.exceptions.HTTPLookupError, ipwhois.exceptions.ASNRegistryError):
            if verbose:
                print("WHOIS: Error looking up IP address {0}".format(ip))
            # Save error report
            j.json_save(traceback.format_exc(limit=2).split(
                '\n'), "err/bad_ip/httplookup_{0}".format(ip))
            return db.pushPair(ip, UNKNOWN)


def getOwnerPairing(addresses):
    with netflow_db.DBManager() as db:
        return {ip: whoisOwner(db, ip) for ip in addresses}


def appendOwnerToData(data, iptype):
    with netflow_db.DBManager() as db:
        for entry in data:
            entry['whois_owner_' + iptype] = whoisOwner(db, entry[iptype])


def appendOwnersToData(data):
    with netflow_db.DBManager() as db:
        for i in progressbar.progressbar(range(len(data)), redirect_stdout=True):
            entry = data[i]
            for iptype in ["dest_ip", "src_ip"]:
                entry['whois_owner_' + iptype] = whoisOwner(db, entry[iptype])


def appendOwnersToEntry(entry):
    with netflow_db.DBManager() as db:
        for iptype in ["dest_ip", "src_ip"]:
            entry['whois_owner_' + iptype] = whoisOwner(db, entry[iptype])


def getDetailedInformation(addresses, force=True, verbose=True):
    pairing = getOwnerPairing(addresses)
    print(
        '\n'.join(
            [ip + "\t" + pairing[ip] for ip in addresses]
        )
    )
