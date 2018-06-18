#!/bin/python3
#Seth Giovanetti

import netflow_util as util

import numpy as np
import matplotlib.pyplot as plt

global_args = {}

def savefig(type, plt):
    import datetime
    import os
    try:
        os.makedirs('./img/')
    except FileExistsError:
        pass
    plt.savefig('./img/' + type + '_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%I_%M_%S%p")) + '.png', bbox_inches="tight")

def doGraph(x,y):
    print()

def top_contributors_percent(predata, percent, flowdir):
    field = 'bytes_in'
    try:
        #Filter records by flow direction
        predata = [i for i in predata if i['flow_dir'] == flowdir ]
        
        #Group records by src_ip
        predata = util.combine_data(predata, lambda a,b: a['src_ip']==b['src_ip'], 'src_ip')
        
        #Convert to sortable ints, and get total
        totalrecords = len(predata)
        total = 0
        for point in predata:
            point[field] = int(point[field])
            total += point[field]
            
        #Get top 10 records by bytes_in
        #Sorts the list by bytes_in, gets the #n... #2, #1 entries, then reverses that list.
        predata = sorted(predata, key=lambda k: k[field])
        
        #Make final data by percent
        data = []
        
        #Map included/total ratio while adding
        included = 0
        while len(predata) > 0 and included < total*(percent/100):
            newrecord = predata.pop()
            included += newrecord[field]
            data.append(newrecord)
            #print({'percent':percent/100,'total':total,'inclulded':included,'totalpercent':total*(percent/100)})
        print("Records included: " + str(len(data)) + '/' + str(totalrecords))

        #Create seperate X and Y arrays based on sort fields
        graphdatay = np.array([point[field] for point in data])
        graphdatax = np.array([point['src_ip'] for point in data])
        print(graphdatax,graphdatay)
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0].keys()]))
        return
    
    if global_args.regress:
        from scipy import stats
        gradient, intercept, r_value, p_value, std_err = stats.linregress(list(range(1,len(graphdatax)+1)),graphdatay)
        mn=np.min(graphdatax)
        mx=np.max(graphdatax)
        x1=np.linspace(mn,mx,500)
        y1=gradient*x1+intercept
        plt.plot(x1,y1,'-r')
    
    # Cumulative counts:
    plt.plot(list(range(1,len(graphdatax)+1)), np.cumsum(graphdatay))

    #Axis labels and formatting
    plt.ylabel('Total ' + field)
    plt.xlabel('Top contributors')
    plt.title('Cumulative traffic, ' + ('incoming' if flowdir == '1' else 'outgoing') + ", top " + str(percent) + '%')

    print('Top ' + str(percent) + '% of contributors: \n' + '\n'.join([graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0,len(graphdatax))]))
    plt.ticklabel_format(style='plain',axis='y',useLocale=True)
    
    #Display
    savefig('top_contributors_percent_'+flowdir,plt)
    print("See window")
    plt.show()

def top_contributors(data, topn, flowdir):
    field = 'bytes_in'
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
    plt.title('Cumulative traffic, ' + ('incoming' if flowdir == '1' else 'outgoing') + ", top " + str(percent) + 'contributors')

    print('Top ' + str(topn) + ' contributors: \n' + '\n'.join([graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0,len(graphdatax))]))
    plt.ticklabel_format(style='plain',axis='y',useLocale=True)
    
    #Display
    savefig('top_contributors_'+flowdir,plt)
    print("See window")
    plt.show()

def top_contributors_noncum(data, topn, flowdir):
    graphdata = []
    field = 'bytes_in'
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
    plt.title('Traffic, ' + ('incoming' if flowdir == '1' else 'outgoing'))

    print('Top ' + str(topn) + ' contributors: \n' + '\n'.join([graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0,len(graphdatax))]))
    plt.ticklabel_format(style='plain',axis='y',useLocale=True)
    
    #Display
    savefig('top_contributors_noncumulative'+flowdir,plt)
    print("See window")
    plt.show()
