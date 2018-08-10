# scp -rp csnetflowdata:/data/netflow/ /data/netflow/
rsync -avP --delete-before --stats csnetflowdata:/data/netflow/ /data/netflow/
