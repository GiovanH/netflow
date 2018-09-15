# scp -rp csnetflowdata:/data/netflow/ /data/netflow/
rsync -avP --delete-before --stats csnfd:/data/netflow/ /data/netflow/ | tee ~/logs/lastget.log
