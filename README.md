# netflow.py

A data handling framework designed for the analysis of Cisco NetFlow traffic reports.

Uses numpy and [mathplotlib.pyplot](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.html)

For maximum portability, the primary development environment uses Anaconda 3.

## Usage

Abstract: Run netflow.py, passing it a file glob, commands to run, and optionally a series of arguments to modify the behavior of the commands.

The most up-to-date usage information can be found by running ``netflow.py --help``



Global arguments:

- field
- files
- ip
- nowhois
- nowindow
- regress
- scaletozero
- verbose

Note to documenters: to regenerate global arguments, run:

`grep -rEo "global_args\.[A-Za-z0-9]+" netflow_graphing.py | cut -c 13- | sort -u`

## Functionality

netflow.py currently supports the following commands:

(Valid directions for [dir] are in and out)

### oniondump

Simply dumps the object data to screen. Used to test the csv reader.

### hist_[dir]

Graphs a non-cumulative histogram of the top contributors.

### top_contributors_[dir]

Graphs a cumulative curve of the top contributors, sorted. Capped by a user-provided integer.

### top_percent_[dir]

Graphs a cumulative curve of the top contributors, sorted. Capped by a user-provided percentage.

### top_percent\_[dir]\_owners

Graphs a cumulative curve of the top contributors, where contributors are grouped by the whois domain owner according to ICANN. Capped by a user-provided percentage.

## Algorithms Used

icannpercent:
1. Start with "data," a list of records.
2. Remove all records whose flow direction does not match the filter.
3. Combine all records whose IP address is the same.
4. Take only the top XX percent of those
5.

## Example output:

For cumulative graphs:

![example](.\docs\example_cumu.png)

For histogram-style graphs:

![example](.\docs\example_contrib.png)
