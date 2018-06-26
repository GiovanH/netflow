#!/bin/python3
#Seth Giovanetti

import netflow_util as util
import netflow_whois as whois

import numpy as np
import matplotlib.pyplot as plt

global_args = {}

#Save a figure as an image.
def savefig(type, plt):
    import datetime
    import os
    try:
        os.makedirs('./img/')
    except FileExistsError:
        pass
    plt.savefig('./img/' + type + '_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%I_%M_%S%p")) + '.png', bbox_inches="tight")

#Abstract function to handle simple X/Y graphing
def doGraph(title,xlabel,x,ylabel,y):
    #Clear any old data on the canvas
    plt.clf()

    #Plot a regression, if asked.
    #This function is unfinished.
    if global_args.regress:
        from scipy import stats
        gradient, intercept, r_value, p_value, std_err = stats.linregress(list(range(1,len(graphdatax)+1)),graphdatay)
        mn=np.min(graphdatax)
        mx=np.max(graphdatax)
        x1=np.linspace(mn,mx,500)
        y1=gradient*x1+intercept
        plt.plot(x1,y1,'-r')
    
    #Plot x and y
    plt.plot(x,y)

    #Axis labels and formatting
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.ticklabel_format(style='plain',axis='y',useLocale=True)
    
    #Save a copy of the figure.
    savefig(util.slugify(global_args.files) + "_" + util.slugify(title), plt)
    
    #Display graph in window, unless running in CLI only mode.
    if not global_args.nowindow:
        print("See window")
        plt.show()

#Graph cumulative traffic of the top %[percent] of traffic contributors. Filtered by flowdir and ip_type.
def top_contributors_percent(predata, percent, flowdir):
    field = 'bytes_in'
    try:
        #Filter out records that do not match the required flow direction.
        predata = [i for i in predata if i['flow_dir'] == flowdir ]
        
        #Group records by ip type
        predata = util.combine_data(predata, lambda a,b: a[global_args.ip_type]==b[global_args.ip_type], global_args.ip_type)
        
        #Convert to sortable ints, and get total data. Required to do percent calculations.
        totalrecords = len(predata)
        total = 0
        for point in predata:
            point[field] = int(point[field])
            total += point[field]
            
        #Get top 10 records by bytes_in
        #Sorts the list by field (bytes_in), gets the #n... #2, #1 entries.
        predata = sorted(predata, key=lambda k: k[field])
        
        #Initialize array for the final data points
        data = []
        #Map included/total ratio while adding
        included = 0
        
        #Calculate top % of data, and use that as the data we graph
        #Until the amount of data we have exceeds %[percent], move a data point into our final list.
        while len(predata) > 0 and included < total*(percent/100):
            newrecord = predata.pop()
            included += newrecord[field]
            data.append(newrecord)
        print("Records included: " + str(len(data)) + '/' + str(totalrecords))

        #Create seperate X and Y arrays based on sort fields
        graphdatay = np.array([point[field] for point in data])
        graphdatax = np.array([point[global_args.ip_type] for point in data])
        print(graphdatax,graphdatay)
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0].keys()]))
        return
    
    #Log which IP addresses account for which rank.
    #Also, run whois comparison if whois is requested.
    if (global_args.whois):
        ip_2_owner = whois.getOwnerPairing(graphdatax);
        
        print(
            'Top ' + str(percent) + '% of contributors: \n' + '\n'.join(
                [graphdatax[i] + "\t" + str(graphdatay[i]) + "\t" + str(ip_2_owner[graphdatax[i]]) for i in range(0,len(graphdatax))]
            )
        )
    else:
        print(
            'Top ' + str(percent) + '% of contributors: \n' + '\n'.join(
                [graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0,len(graphdatax))]
            )
        )
    
    #Do final graph.
    doGraph(
        'Cumulative traffic, ' + ('incoming' if flowdir == '1' else 'outgoing') + ", top " + str(percent) + '%, by ' + global_args.ip_type,
        'Top contributors',
        list(range(1,len(graphdatax)+1)),
        'Total ' + field,
        np.cumsum(graphdatay)
    )

#Graph cumulative traffic of the top [topn] of traffic contributors. Filtered by flowdir and ip_type.
def top_contributors(data, topn, flowdir):
    field = global_args.field
    try:
        #Filter records by flow direction
        data = [i for i in data if i['flow_dir'] == flowdir ]
        
        #Group records by src_ip
        data = util.combine_data(data, lambda a,b: a[global_args.ip_type]==b[global_args.ip_type], global_args.ip_type)
        
        #Convert to sortable ints
        for point in data:
            point[field] = int(point[field])
            
        #Get top N records by bytes_in
        #Sorts the list by bytes_in, gets the #n... #2, #1 entries, then reverses that list.
        data = sorted(data, key=lambda k: k[field])[-topn:][::-1]

        #Create seperate X and Y arrays based on sort fields
        graphdatay = np.array([point[field] for point in data])
        graphdatax = np.array([point[global_args.ip_type] for point in data])
        print(graphdatax,graphdatay)
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0].keys()]))
        return
    
    print('Top ' + str(topn) + ' contributors: \n' + '\n'.join([graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0,len(graphdatax))]))
    
    doGraph(
        'Cumulative traffic, ' + ('incoming' if flowdir == '1' else 'outgoing') + ", top " + str(topn) + ' by ' + global_args.ip_type,
        'Top contributors',
        list(range(1,len(graphdatax)+1)),
        'Total ' + field,
        np.cumsum(graphdatay)
    )

def top_contributors_noncum(data, topn, flowdir):
    graphdata = []
    field = 'bytes_in'
    try:
        #Filter records by flow direction
        data = [i for i in data if i['flow_dir'] == flowdir ]
        
        #Group records by src_ip
        data = util.combine_data(data, lambda a,b: a[global_args.ip_type]==b[global_args.ip_type], global_args.ip_type)
        
        #Convert to sortable ints
        for point in data:
            point[field] = int(point[field])
            
        #Get top 10 records by bytes_in
        #Sorts the list by bytes_in, gets the #n... #2, #1 entries, then reverses that list.
        data = sorted(data, key=lambda k: k[field])[-topn:][::-1]

        #Create seperate X and Y arrays based on sort fields
        graphdatay = np.array([point[field] for point in data])
        graphdatax = np.array([point[global_args.ip_type] for point in data])
        print(graphdatax,graphdatay)
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0].keys()]))
        return
    
    print('Top ' + str(topn) + ' contributors: \n' + '\n'.join([graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0,len(graphdatax))]))
    
    doGraph(
        'Traffic, ' + ('incoming' if flowdir == '1' else 'outgoing') + ', by ' + global_args.ip_type,
        'Top N contributor',
        list(range(1,len(graphdatax)+1)),
        'Total ' + field,
        graphdatay
    )