"C:/ProgramData/Anaconda3/python.exe" -i  netflow.py \
    --percent 70 \
    --nowindow \
    --verbose \
    --scaletozero \
    --regress 1\
    "../20180110/*0.csv" \
    c

for degree in [2, 3, 4, 5, 6]:
    args.regress = degree
    for a in ['out', 'in']:
        for b in ['dest', 'src']:
            o = "_".join(['icannpercent', a, b])
            print(o)
            options[o]()
