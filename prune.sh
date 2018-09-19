find ./out/* -type f -mtime +21 -exec rm -v {} 2>/dev/null \;
find ./out/* -type d -exec rmdir {} 2>/dev/null \;
