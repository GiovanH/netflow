#!/bin/bash

# scp -rp csnetflowdata:/data/netflow/ /data/netflow/
max_storage_days=7

#Delete outdated files
find /data/netflow/ -mtime +$(($max_storage_days+2)) -exec rm -rv {} \;

#Get new files
ssh -qx csnfd "find /data/netflow/* -type f -mtime -$max_storage_days -print0" |\
    rsync --size-only --from0 --files-from=- -ri "csnfd:/" /
