# scp -rp csnetflowdata:/data/netflow/ /data/netflow/
max_storage_days=7

#Delete outdated files
find /data/netflow/ -mtime +$max_storage_days -exec rm -rv {} \;

#Get new files
ssh -qx csnfd "find /data/netflow/* -type d -mtime -$max_storage_days -print0" | \
    rsync --from0 --files-from=- -riv "csnfd:/" /data/netflow/
