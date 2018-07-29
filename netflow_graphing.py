#!/bin/python3
# Seth Giovanetti

import netflow_util as util
import netflow_whois as whois
from pprint import pformat

import numpy as np
import matplotlib.pyplot as plt

import warnings

# "It's okay not to have enough data."
warnings.simplefilter('ignore', np.RankWarning)


global_args = {}


# Save a figure as an image.
def savefig(glob, type, plt, titleappend=""):
    import os
    destpath = './out/' + util.sluggify(glob) + "/" + util.sluggify(type) + '/'
    try:
        os.makedirs(destpath)
    except FileExistsError:
        pass
    # plt.savefig(destpath + str(datetime.datetime.now().strftime("%Y-%m-%d_%I_%M_%S%p")
    #                            ) + '.png', bbox_inches="tight")
    plt.savefig(destpath + 'graph' + titleappend + '.png', bbox_inches="tight")


def savelog(glob, type, text, titleappend=""):
    import os
    destpath = './out/' + util.sluggify(glob) + "/" + util.sluggify(type) + '/'
    try:
        os.makedirs(destpath)
    except FileExistsError:
        pass
    # with open(destpath + str(datetime.datetime.now().strftime("%Y-%m-%d_%I_%M_%S%p") + titleappend) + '.log', "w") as file:
    with open(destpath + 'log' + titleappend + '.log', "w") as file:
        file.write(type + "\n")
        file.write(text)


def graphText(textstr, plt):
    print(textstr)
    fig, ax = plt.subplots()

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # place a text box in upper left in axes coords
    # ax.text(0, 2, textstr, transform=ax.transAxes, fontsize=12,
    #        va='top', wrap=True, bbox=props)
    # ax.text(.1, .1, textstr)
    ax.text(-0.1, -0.1, textstr.replace("\t", ": "), transform=ax.transAxes, va='top')


def doGraphMeta(command, title, xlabel, ylabel, saveImage=True, clear=True):

    # Axis labels and formatting
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.ticklabel_format(style='plain', axis='y', useLocale=True)

    # Formatting settings
    if global_args.scaletozero:
        plt.ylim(ymin=0)

    if saveImage:
        # Save a copy of the figure.
        savefig(global_args.files, command, plt, titleappend=("_regression_" +
                                                              str(global_args.regress) if global_args.regress is not None else ''))

    # Display graph in window, unless running in CLI only mode.
    if not global_args.nowindow:
        print("See window")
        plt.show()

    # Clear any old data on the canvas
    if clear:
        plt.clf()
        plt.close()
# Abstract function to handle simple X/Y graphing


def doGraph(command, title, xlabel, x, ylabel, y, clear=True, saveImage=True, regress=None, points=True):
    # Verbose data save
    if global_args.verbose:
        savelog(global_args.files, command, pformat(
                [[x[i], y[i]] for i in range(0, len(x))]
                ), titleappend="_verbose_points"
                )
    # Plot a regression, if asked.
    # This function is unfinished.
    if regress is not None:

        # If we're going to do data regression, we want to do a normal graph first.
        # This has the side effect of "using up" any data that was already on the canvas, like IP logs. That's fine.
        doGraph(command, title, xlabel, x, ylabel, y,
                clear=clear, saveImage=saveImage, regress=None)

        print("Data regression with degree " + str(regress))
        fit = np.polyfit(x, y, regress)  # Get the polynomial fit, e.g. the polynomial coefficients.
        # Create a formatted string to represent the function. This is only for display.
        polynomstr = util.represent_poly([round(o, 3) for o in fit])

        print(polynomstr)
        # Print the formula on the bottom right corner.
        fig, ax = plt.subplots()
        ax.text(0.95, 0.01, '$y=' + polynomstr + '$',
                verticalalignment='bottom', horizontalalignment='right',
                transform=ax.transAxes)

        # Create a function for the polynomial. fit_fn(x) ~= y(x)
        fit_fn = np.poly1d(fit)
        # Plot the line
        plt.plot(x, fit_fn(x), '--k', linestyle='solid', color='red')

    if points:
        # Plot x and y as points.
        plt.plot(x, y, color='blue', marker='o', linestyle='none',
                 linewidth=2, markersize=3)  # Blue circles, solid lines
    else:
        # Plot x and y as a line.
        plt.plot(x, y, color='blue', marker='o', linestyle='solid',
                 linewidth=2, markersize=3)  # Blue circles, solid lines

    doGraphMeta(command, title, xlabel, ylabel, saveImage=saveImage, clear=clear)

# Graph cumulative traffic of the top %[percent] of traffic contributors. Filtered by flowdir and ip_type.


def graph_ippercent(predata, percent, flowdir, ip_type):
    field = 'bytes_in'
    command = "_".join(
        ['ippercent', str(percent), ('incoming' if flowdir == '1' else 'outgoing'), ip_type])
    try:
        # Filter out records that do not match the required flow direction.
        predata = [i for i in predata if i['flow_dir'] == flowdir]

        # Group records by ip type
        predata = util.simple_combine_data(predata, ip_type)

        # Convert to sortable ints, and get total data. Required to do percent calculations.
        totalrecords = len(predata)
        total = 0
        for point in predata:
            point[field] = int(point[field])
            total += point[field]

        # Get top 10 records by bytes_in
        # Sorts the list by field (bytes_in), gets the #n... #2, #1 entries.
        predata = sorted(predata, key=lambda k: k[field])

        # Initialize array for the final data points
        data = []
        # Map included/total ratio while adding
        included = 0

        # Calculate top % of data, and use that as the data we graph
        # Until the amount of data we have exceeds %[percent], move a data point into our final list.
        while len(predata) > 0 and included < total*(percent/100):
            newrecord = predata.pop()
            included += newrecord[field]
            data.append(newrecord)
        print("Records included: " + str(len(data)) + '/' + str(totalrecords))

        if global_args.compress_size is not None:
            for point in data:
                point['bytes_in'] = int(point['bytes_in'])/global_args.compress_size

        # Create seperate X and Y arrays based on sort fields
        graphdatay = np.array([point[field] for point in data])
        graphdatax = np.array([point[ip_type] for point in data])
        # print(graphdatax,graphdatay)
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0].keys()]))
        return

    graphtitle = 'Cumulative traffic, ' + \
        ('incoming' if flowdir == '1' else 'outgoing') + \
        ", top " + str(percent) + '%, by ' + ip_type

    logtxt = ""
    # Log which IP addresses account for which rank.
    # Also, run whois comparison if whois is requested.
    if (not global_args.nowhois):
        ip_2_owner = whois.getOwnerPairing(graphdatax)

        logtxt = 'Top ' + str(percent) + '% of contributors: \n' + '\n'.join(
            [graphdatax[i] + "\t" + str(graphdatay[i]) + "\t" + str(ip_2_owner[graphdatax[i]])
             for i in range(0, len(graphdatax))]
        )

    else:
        logtxt = 'Top ' + str(percent) + '% of contributors: \n' + pformat(
            [graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0, len(graphdatax))]
        )

    graphText(logtxt, plt)
    savelog(global_args.files, command, logtxt)
    # Do final graph.
    doGraph(
        command,
        graphtitle,
        'Top contributors',
        list(range(1, len(graphdatax)+1)),
        'Total ' + field,
        np.cumsum(graphdatay),
        regress=global_args.regress
    )

# Graph cumulative traffic of the top %[percent] of traffic contributors. Filtered by flowdir and ip_type.


def graph_icannpercent(data, percent, flowdir, ip_type):
    field = 'bytes_in'
    command = "_".join(['icannpercent', str(percent),
                        ('incoming' if flowdir == '1' else 'outgoing'), ip_type])
    graphtitle = 'Cumulative traffic, ' + \
        ('incoming' if flowdir == '1' else 'outgoing') + \
        ", top " + str(percent) + '% of owners, by ' + ip_type
    try:
        # Filter out records that do not match the required flow direction.
        data = [i for i in data if i['flow_dir'] == flowdir]

        # Group records by ip
        data = util.simple_combine_data(data, ip_type)

        # Calculate total for percent calculations
        total = 0
        for point in data:
            point[field] = int(point[field])
            total += point[field]

        # Take top percent
        data = util.top_percent(data, percent, field, total)

        # Append whois data to this reduced data set
        whois.appendOwnerData(data, ip_type)

        # Verbose data save
        if global_args.verbose:
            savelog(global_args.files, command, pformat(data), titleappend="_verbose_ip_data"
                    )

        # Group by whois data
        data = util.simple_combine_data(data, "whois_owner_" + ip_type)

        # Sort reduced data set
        data = sorted(data, key=lambda k: k[field])[::-1]

        if global_args.compress_size is not None:
            for point in data:
                point['bytes_in'] = int(point['bytes_in'])/global_args.compress_size

        # Create seperate X and Y arrays based on sort fields
        graphdatay = np.array([point[field] for point in data])
        graphdatax = np.array([point["whois_owner_" + ip_type] for point in data])
        # print(graphdatax,graphdatay) #TODO: IF verbose
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0].keys()]))
        return

    # Log which IP addresses account for which rank.
    # Also, run whois comparison if whois is requested.

    logtxt = 'Top ' + str(percent) + '% of contributors: \n' + '\n'.join(
        [graphdatax[i] + "\t" + str(graphdatay[i]) + "\t" for i in range(0, len(graphdatax))]
    )

    graphText(logtxt, plt)
    savelog(global_args.files, command, logtxt)

    # Do final graph.
    doGraph(
        command,
        graphtitle,
        'Top contributors',
        list(range(1, len(graphdatax)+1)),
        'Total ' + field,
        np.cumsum(graphdatay),
        regress=global_args.regress
    )


def graph_icannstacktime(data, topn, flowdir, ip_type):
    command = "_".join(['icannstacktime', str(topn),
                        ('incoming' if flowdir == '1' else 'outgoing'), ip_type])
    graphtitle = 'Cumulative traffic, ' + \
        ('incoming' if flowdir == '1' else 'outgoing') + \
        ", top " + str(topn) + ' owners, by ' + ip_type

    # Filter out records that do not match the required flow direction.
    data = [i for i in data if i['flow_dir'] == flowdir]

    # We can't group by IP yet, because that would discard time data.

    # Get top records by bytes_in
    # Sorts the list by bytes_in, gets the #n... #2, #1 entries, then reverses that list.
    data = sorted(data, key=lambda k: k['bytes_in'])[-topn:][::-1]

    # Append whois data to this reduced data set
    whois.appendOwnerData(data, ip_type)

    # Verbose data save
    if global_args.verbose:
        savelog(global_args.files, command, pformat(data), titleappend="_verbose_ip_data"
                )

    # Group by whois data, retaining time info
    data = util.multi_combine_data(data, ["whois_owner_" + ip_type, 'time'])

    # Sort reduced data set
    data = sorted(data, key=lambda k: k['bytes_in'])[::-1]

    if global_args.compress_size is not None:
        for point in data:
            point['bytes_in'] = int(point['bytes_in'])/global_args.compress_size

    # graphText(logtxt, plt)
    # savelog(global_args.files, command, logtxt)

    #Graphdata.  dff
    # Our X values will be TIME.
    data = sorted(data, key=lambda k: k['time'])
    x = [point['time'] for point in data]
    # print(pformat(x))
    # We will have a list of Y values.
    # Each y list represents one whois owner.
    whoisowners = set([point["whois_owner_" + ip_type] for point in data])
    ys = []
    for owner in whoisowners:
        y = []
        for time in x:
            y.append(
                sum(
                    [point['bytes_in'] for point in data if point["whois_owner_" + ip_type] == owner and point["time"] == time]
                )
            )
        ys.append(y)

    if global_args.verbose:
        savelog(global_args.files, command, pformat(
            [x,ys]
        ), titleappend="_verbose_points"
        )

    y = np.vstack(ys)
    # Do final graph.
    fig, ax = plt.subplots()
    ax.stackplot(x, y, labels=whoisowners)
    ax.legend(loc=2)
    doGraphMeta(
        command,
        graphtitle,
        'Top contributors',
        'Total ' + 'bytes_in'
    )

# Graph cumulative traffic of the top [topn] of traffic contributors. Filtered by flowdir and ip_type.


def graph_top(data, topn, flowdir, ip_type):
    field = global_args.field
    command = "_".join(['top', str(topn), ('incoming' if flowdir == '1' else 'outgoing'), ip_type])
    try:
        # Filter records by flow direction
        data = [i for i in data if i['flow_dir'] == flowdir]

        # Group records by src_ip
        data = util.simple_combine_data(data, ip_type)

        # Convert to sortable ints
        for point in data:
            point[field] = int(point[field])

        # Get top N records by bytes_in
        # Sorts the list by bytes_in, gets the #n... #2, #1 entries, then reverses that list.
        data = sorted(data, key=lambda k: k[field])[-topn:][::-1]

        # Create seperate X and Y arrays based on sort fields
        graphdatay = np.array([point[field] for point in data])
        graphdatax = np.array([point[ip_type] for point in data])
        # print(graphdatax,graphdatay)
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0].keys()]))
        return

    graphtitle = 'Cumulative traffic, ' + \
        ('incoming' if flowdir == '1' else 'outgoing') + ", top " + str(topn) + ' by ' + ip_type

    logtxt = 'Top ' + str(topn) + ' contributors: \n' + \
        '\n'.join([graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0, len(graphdatax))])

    graphText(logtxt, plt)
    savelog(global_args.files, command, logtxt)
    doGraph(
        command,
        graphtitle,
        'Top contributors',
        list(range(1, len(graphdatax)+1)),
        'Total ' + field,
        np.cumsum(graphdatay),
        regress=global_args.regress
    )


def graph_hist(data, topn, flowdir, ip_type):
    graphdata = []
    command = "_".join(['hist', str(topn), ('incoming' if flowdir == '1' else 'outgoing'), ip_type])
    field = 'bytes_in'
    try:
        # Filter records by flow direction
        data = [i for i in data if i['flow_dir'] == flowdir]

        # Group records by src_ip
        data = util.simple_combine_data(data, ip_type)

        # Convert to sortable ints
        for point in data:
            point[field] = int(point[field])

        # Get top 10 records by bytes_in
        # Sorts the list by bytes_in, gets the #n... #2, #1 entries, then reverses that list.
        data = sorted(data, key=lambda k: k[field])[-topn:][::-1]

        if global_args.compress_size is not None:
            for point in data:
                point['bytes_in'] = int(point['bytes_in'])/global_args.compress_size

        # Create seperate X and Y arrays based on sort fields
        graphdatay = np.array([point[field] for point in data])
        graphdatax = np.array([point[ip_type] for point in data])
        # print(graphdatax,graphdatay)
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0].keys()]))
        return

    graphtitle = 'Traffic, ' + ('incoming' if flowdir == '1' else 'outgoing') + ', by ' + ip_type

    logtxt = 'Top ' + str(topn) + ' contributors: \n' + \
        '\n'.join([graphdatax[i] + "\t" + str(graphdatay[i]) for i in range(0, len(graphdatax))])

    graphText(logtxt, plt)
    savelog(global_args.files, command, logtxt)
    doGraph(
        command,
        graphtitle,
        'Top N contributor',
        list(range(1, len(graphdatax)+1)),
        'Total ' + field,
        graphdatay,
        regress=global_args.regress
    )
