#!/bin/python3
#Seth Giovanetti

import netflow_util as util

def histo(data, field):
    import numpy as np
    import matplotlib.pyplot as plt
    graphdata = []
    try:
        graphdata = [point[field] for sheet in data for point in sheet]
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0][0].keys()]))
        return
    n_bins = 100
    n, bins, patches = plt.hist(graphdata, n_bins, density=True, facecolor='g', alpha=0.75)
    plt.xlabel(field)
    plt.ylabel('Probability')
    plt.title('Histogram of ' + field)
    #plt.grid(True)
    print("See window")
    plt.show()


def cumutop(indata):
    import numpy as np
    import matplotlib.pyplot as plt
    graphdata = []
    field = 'bytes_in' #What field our y-axis data comes from
    topn = 50 #We care about the top N records
    data = indata
    try:
        #Group records by src_ip
        data = util.combine_data(data, lambda a,b: a['src_ip']==b['src_ip'], 'src_ip')
        
        #Convert to sortable ints
        for point in data:
            point[field] = int(point[field])
            
        #Get top 10 records by bytes_in
        #Sorts the list by bytes_in, gets the #n... #2, #1 entries, then reverses that list.
        data = sorted(data, key=lambda k: k[field])[-topn:][::-1]

        #Create seperate X and Y arrays based on sort fields
        graphdatay = np.array([point[field] for point in data])
        graphdatax = np.array([point['src_ip'] for point in data])
        print(graphdatax,graphdatay)
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0].keys()]))
        return
    
    # Cumulative counts:
    plt.plot(list(range(1,topn+1)), np.cumsum(graphdatay))
    #sorted_data = np.sort(graphdatay)  # Or data.sort(), if data can be modified
    #plt.step(sorted_data,np.arange(sorted_data.size))

    #Axis labels and formatting
    plt.ylabel('Total')
    plt.title('Cumulative ' + field)

    print('Top ' + str(topn) + ' contributors: \n' + '\n'.join([graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0,len(graphdatax))]))
    plt.ticklabel_format(style='plain',axis='y',useLocale=True)
    
    #Display
    print("See window")
    plt.show()


def cumu(data, field):
    import numpy as np
    import matplotlib.pyplot as plt
    graphdata = []
    try:
        #Compress data
        data = util.combine_data(data, lambda a,b: a['_time'][:-12]==b['_time'][:-12], '_time')

        #Create seperate X and Y arrays based on sort fields        
        graphdatay = [int(point[field]) for point in data]
        graphdatax = [point['_time'] for point in data]

        #Sort data by time? Not needed with data compression
        #graphdatax, graphdatay = (np.array(t) for t in zip(*sorted(zip(graphdatax, graphdatay))))
        print(graphdatax,graphdatay)
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0].keys()]))
        return
    # Cumulative counts:
    plt.step(graphdatax,np.cumsum(graphdatay))

    #Axis labels and formatting
    plt.ylabel('Total')
    plt.title('Cumulative ' + field)

    #Display
    print("See window")
    plt.show()
