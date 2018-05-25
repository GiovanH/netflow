#!/bin/python3
#Seth Giovanetti

import netflow_util as util
import copy

global_args = {}

def savefig(type, plt):
    import datetime
    import os
    try:
        os.makedirs('./img/')
    except FileExistsError:
        pass
    plt.savefig('./img/' + type + '_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%I_%M_%S%p")) + '.png', bbox_inches="tight")


def top_contributors(indata, topn, flowdir):
    import numpy as np
    import matplotlib.pyplot as plt
    graphdata = []
    field = 'bytes_in'
    data = copy.deepcopy(indata)
    try:
        #Filter records by flow direction
        data = [i for i in data if i['flow_dir'] == flowdir ]
        
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
    plt.plot(list(range(1,len(graphdatax)+1)), np.cumsum(graphdatay))

    #Axis labels and formatting
    plt.ylabel('Total ' + field)
    plt.xlabel('Top contributors')
    #Todo: Verify flow dir
    plt.title('Cumulative traffic, ' + ('incoming' if flowdir == '1' else 'outgoing'))

    print('Top ' + str(topn) + ' contributors: \n' + '\n'.join([graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0,len(graphdatax))]))
    plt.ticklabel_format(style='plain',axis='y',useLocale=True)
    
    #Display
    savefig('top_contributors_'+flowdir,plt)
    print("See window")
    plt.show()

def top_contributors_noncum(indata, topn, flowdir):
    import numpy as np
    import matplotlib.pyplot as plt
    graphdata = []
    field = 'bytes_in'
    data = copy.deepcopy(indata)
    try:
        #Filter records by flow direction
        data = [i for i in data if i['flow_dir'] == flowdir ]
        
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
    plt.step(list(range(1,len(graphdatax)+1)), graphdatay)

    #Axis labels and formatting
    plt.ylabel(field)
    plt.xlabel('Top N contributor')
    #Todo: Verify flow dir
    plt.title('Traffic, ' + ('incoming' if flowdir == '1' else 'outgoing'))

    print('Top ' + str(topn) + ' contributors: \n' + '\n'.join([graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0,len(graphdatax))]))
    plt.ticklabel_format(style='plain',axis='y',useLocale=True)
    
    #Display
    savefig('top_contributors_noncumulative'+flowdir,plt)
    print("See window")
    plt.show()
