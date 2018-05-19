#!/bin/python3
#Seth Giovanetti

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


def cumu(data, field):
    import numpy as np
    import matplotlib.pyplot as plt
    graphdata = []
    try:
        graphdatay = np.array([int(point[field]) for sheet in data for point in sheet])
        graphdatax = [point['_time'] for sheet in data for point in sheet]
        print([graphdatax,graphdatay])
        #Sort by time
        graphdatax, graphdatay = (np.array(t) for t in zip(*sorted(zip(graphdatax, graphdatay))))
        print([graphdatax,graphdatay])
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0][0].keys()]))
        return
    #n_bins = 50

    # Cumulative counts:
    plt.step(graphdatax,np.cumsum(graphdatay))
    #sorted_data = np.sort(graphdatay)  # Or data.sort(), if data can be modified
    #plt.step(sorted_data,np.arange(sorted_data.size))
    plt.ylabel('Total')
    plt.title('Cumulative ' + field)
    print("See window")
    plt.show()
