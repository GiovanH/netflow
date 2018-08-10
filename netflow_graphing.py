#!/bin/python3
# Seth Giovanetti

import netflow_util as util
import netflow_whois as whois
from pprint import pformat

import numpy as np
import matplotlib.pyplot as plt

import warnings

# "It's okay not to have enough data for a good regression."
warnings.simplefilter('ignore', np.RankWarning)

# Initialize global_args
global_args = {}


# Saves a figure as an image. Uses glob and titleappend for naming.
def savefig(glob, type, plt, titleappend=""):
    import os
    # Crafts base path
    destpath = './out/' + util.sluggify(glob) + "/" + util.sluggify(type) + '/'
    # Make necessary directories, if they don't exist.
    try:
        os.makedirs(destpath)
    except FileExistsError:
        pass
    # Save figure
    fig = plt.gcf()
    fig.set_size_inches(10, 6)
    plt.savefig(destpath + 'graph' + titleappend + '.png', bbox_inches="tight")


# Save a text log. Uses glob and titleappend for naming.
def savelog(glob, type, text, titleappend=""):
    import os
    # Crafts base path
    destpath = './out/' + util.sluggify(glob) + "/" + util.sluggify(type) + '/'
    # Make necessary directories, if they don't exist.
    try:
        os.makedirs(destpath)
    except FileExistsError:
        pass
    # Save text file
    with open(destpath + 'log' + titleappend + '.log', "w") as file:
        file.write(type + "\n")
        file.write(text)


# Add some text to the graph.
def graphText(textstr, plt):
    # Echo string to console.
    print(textstr)
    # Pull out figure and axis variables.
    fig, ax = plt.subplots()
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # place a text box in upper left in axes coords
    ax.text(-0.1, -0.1, textstr.replace("\t", ": "), transform=ax.transAxes, va='top')


# Does everything but plot the graph. Useful if you don't want to use plt.plot.
# This should be run last, as it also handles saving the graph as an image.
def doGraphMeta(command, title, xlabel, ylabel, saveImage=True, clear=True, titleappend=""):
    # Apply axis labels, graph title, and tick formatting.
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.ticklabel_format(style='plain', axis='y', useLocale=True)

    # Formatting settings.
    # Scale to zero if asked, otherwise, this defaults to autoscale.
    if global_args.scaletozero:
        plt.ylim(ymin=0)

    # Save a copy of the figure, if requested.
    if saveImage:
        savefig(global_args.files, command, plt, titleappend=titleappend)

    # Display graph in window, unless running in CLI only mode.
    if not global_args.nowindow:
        print("See window")
        plt.show()

    # Clear any old data on the canvas
    if clear:
        plt.clf()
        plt.close()


# Abstract function to handle simple X/Y graphing
def doGraph(command, title, xlabel, x, ylabel, y, clear=True, saveImage=True, regress=None, points=True, titleappend=""):
    # Verbose data save
    if global_args.verbose:
        savelog(global_args.files, command, pformat(
                [[x[i], y[i]] for i in range(0, len(x))]
                ), titleappend="_verbose_points"
                )
    # Plot a regression, if asked.
    if regress is not None:
        # If we're going to do data regression, we want to do a normal graph first.
        # This has the side effect of "using up" any data that was already on the canvas, like IP logs. That's fine.
        doGraph(command, title, xlabel, x, ylabel, y,
                clear=clear, saveImage=saveImage, regress=None)

        # This file's title should have a regression title
        titleappend += "_regression"

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

    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    doGraphMeta(command, title, xlabel, ylabel, saveImage=saveImage, clear=clear, titleappend=titleappend)


# Graph cumulative traffic of the top %[percent] of traffic contributors. Filtered by flowdir and ip_type.
def graph_ippercent(data, percent, flowdir, ip_type):
    # Write a unique name for this command.
    command = "_".join(
        ['ippercent', str(percent), ('incoming' if flowdir == '1' else 'outgoing'), ip_type])
    print(command)
    # Write graph title based on arguments.
    graphtitle = 'Cumulative traffic, ' + \
        ('incoming' if flowdir == '1' else 'outgoing') + \
        ", top " + str(percent) + '%, by ' + ip_type

    # Filter out records that do not match the required flow direction.
    data = [i for i in data if i['flow_dir'] == flowdir]

    # Group records by ip type
    data = util.simple_combine_data(data, ip_type)

    # Take the top percent of data, by bytes_in
    data = util.top_percent(data, percent, 'bytes_in')

    # Compress bytes, if requested.
    if global_args.compress_size is not None:
        util.compress_bytes(data, global_args.compress_size)

    # Create seperate X and Y arrays based on sort fields
    graphdatay = np.array([point['bytes_in'] for point in data])
    graphdatax = np.array([point[ip_type] for point in data])

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
        'Total ' + 'bytes_in',
        np.cumsum(graphdatay),
        regress=global_args.regress
    )


# Graph cumulative traffic of the top %[percent] of traffic contributors. Filtered by flowdir and ip_type.
def graph_icannpercent(data, percent, flowdir, ip_type):
    # Write a unique name for this command.
    command = "_".join(['icannpercent', str(percent),
                        ('incoming' if flowdir == '1' else 'outgoing'), ip_type])
    print(command)
    # Write graph title based on function arguments
    graphtitle = 'Cumulative traffic, ' + \
        ('incoming' if flowdir == '1' else 'outgoing') + \
        ", top " + str(percent) + '% of owners, by ' + ip_type

    # Filter out records that do not match the required flow direction.
    data = [i for i in data if i['flow_dir'] == flowdir]

    # Group records by IP address only.
    data = util.simple_combine_data(data, ip_type)
    # Append whois data to the full data set
    whois.appendOwnerData(data, ip_type)
    # Group records by whois owner.
    data = util.simple_combine_data(data, "whois_owner_" + ip_type)

    # Take top percent
    data = util.top_percent(data, percent, 'bytes_in')

    # Verbose data save
    if global_args.verbose:
        savelog(global_args.files, command, pformat(data), titleappend="_verbose_ip_data")

    # Sort reduced data set
    data = sorted(data, key=lambda k: k['bytes_in'])[::-1]

    if global_args.compress_size is not None:
        util.compress_bytes(data, global_args.compress_size)

    # Create seperate X and Y arrays based on sort fields
    graphdatay = np.array([point['bytes_in'] for point in data])
    graphdatax = np.array([point["whois_owner_" + ip_type] for point in data])

    # Log which whois entities account for which rank.
    logtxt = 'Top ' + str(percent) + '% of contributors: \n' + '\n'.join(
        [graphdatax[i] + "\t" + str(graphdatay[i]) + "\t" for i in range(0, len(graphdatax))]
    )

    # Add text to graph and log file
    graphText(logtxt, plt)
    savelog(global_args.files, command, logtxt)

    # Do final graph.
    doGraph(
        command,
        graphtitle,
        'Top contributors',
        list(range(1, len(graphdatax)+1)),
        'Total ' + 'bytes_in',
        np.cumsum(graphdatay),
        regress=global_args.regress
    )


def graph_icannstacktime(data, topn, flowdir, ip_type, overlap=True, stack=True):
    command = "_".join(['icannstacktime', str(topn),
                        ('incoming' if flowdir == '1' else 'outgoing'), ip_type])
    print(command)
    graphtitle = 'Traffic, ' + \
        ('incoming' if flowdir == '1' else 'outgoing') + \
        ", top " + str(topn) + ' owners, by ' + ip_type

    # Filter out records that do not match the required flow direction.
    data = [i for i in data if i['flow_dir'] == flowdir]

    # Group by IP, retaining time info
    data = util.multi_combine_data(data, [ip_type, 'time'])
    # Append whois data to this reduced data set
    whois.appendOwnerData(data, ip_type)
    # Group by whois data, retaining time info
    data = util.multi_combine_data(data, ["whois_owner_" + ip_type, 'time'])

    if global_args.compress_size is not None:
        util.compress_bytes(data, global_args.compress_size)

    # graphText(logtxt, plt)
    # savelog(global_args.files, command, logtxt)

    # Our X values will be TIME.
    # data = sorted(data, key=lambda k: k['time'])
    x = list(range(0, 24))
    # print(pformat(x))

    # We will have a list of Y values.
    # Each y list represents one whois owner.
    whoisowners = list(set(
        [
            point["whois_owner_" + ip_type] for point in sorted(
                # We care about the top topn OVERALL, not the top for any time, so we need to strip time data.
                util.simple_combine_data(data, "whois_owner_" + ip_type), key=lambda k: k['bytes_in']
            )[-topn:][::-1]
        ]
    ))

    # Do final graph, incrementally building lines.
    fig, ax = plt.subplots()
    ys = []
    totalbytes = 0
    for owner in whoisowners:
        y = []
        for time in x:
            s = 0.0
            for point in data:
                totalbytes += point['bytes_in']
                if point["whois_owner_" + ip_type] == owner and int(point["time"]) == time:
                    s += point['bytes_in']
            y.append(s)
        if overlap:
            plt.plot(x, y, label=owner)
        ys.append(y)

    # Get line for the total
    #if overlap:
    total_y = []
    for time in x:
        s = 0.0
        for point in data:
            if int(point["time"]) == time:
                s += point['bytes_in']
        total_y.append(s)
    plt.plot(x, total_y, label="Total")

    if global_args.verbose:
        savelog(global_args.files, command, pformat(
            [x, ys]
        ), titleappend="_verbose_points"
        )

    if overlap:
        plt.xticks(np.arange(min(x), max(x)+1, 1.0))
        plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        ax.legend(loc='best')

        doGraphMeta(
            command,
            graphtitle,
            'Time (Hours, 0-23)',
            'Total ' + util.localize_bytes(global_args.compress_size),
            titleappend="_overlap"
        )

    if stack:
        # Let's also do a stack graph.
        fig, ax = plt.subplots()
        ax.stackplot(x, np.vstack(ys), labels=whoisowners)
        plt.xticks(np.arange(min(x), max(x)+1, 1.0))
        plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        ax.legend(loc='best')

        # Add in the total line
        plt.plot(x, total_y, label="Total")
        doGraphMeta(
            command,
            graphtitle + " (Stack)",
            'Time (Hours, 0-23)',
            'Total ' + util.localize_bytes(global_args.compress_size),
            titleappend="_stack"
        )


# Graph cumulative traffic of the top [topn] of traffic contributors. Filtered by flowdir and ip_type.
def graph_top(data, topn, flowdir, ip_type):
    command = "_".join(['top', str(topn), ('incoming' if flowdir == '1' else 'outgoing'), ip_type])
    print(command)
    # Filter records by flow direction
    data = [i for i in data if i['flow_dir'] == flowdir]

    # Group records by src_ip
    data = util.simple_combine_data(data, ip_type)

    # Get top N records by bytes_in
    # Sorts the list by bytes_in, gets the #n... #2, #1 entries, then reverses that list.
    data = sorted(data, key=lambda k: k['bytes_in'])[-topn:][::-1]

    # Create seperate X and Y arrays based on sort fields
    graphdatay = np.array([point['bytes_in'] for point in data])
    graphdatax = np.array([point[ip_type] for point in data])
    # print(graphdatax,graphdatay)

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
        'Total ' + util.localize_bytes(global_args.compress_size),
        np.cumsum(graphdatay),
        regress=global_args.regress
    )


def graph_hist(data, topn, flowdir, ip_type):
    command = "_".join(['hist', str(topn), ('incoming' if flowdir == '1' else 'outgoing'), ip_type])
    print(command)
    # Filter records by flow direction
    data = [i for i in data if i['flow_dir'] == flowdir]

    # Group records by src_ip
    data = util.simple_combine_data(data, ip_type)

    # Get top 10 records by bytes_in
    # Sorts the list by bytes_in, gets the #n... #2, #1 entries, then reverses that list.
    data = sorted(data, key=lambda k: k['bytes_in'])[-topn:][::-1]

    if global_args.compress_size is not None:
        util.compress_bytes(data, global_args.compress_size)

    # Create seperate X and Y arrays based on sort fields
    graphdatay = np.array([point['bytes_in'] for point in data])
    graphdatax = np.array([point[ip_type] for point in data])
    # print(graphdatax,graphdatay)

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
        'Total ' + util.localize_bytes(global_args.compress_size),
        graphdatay,
        regress=global_args.regress
    )
