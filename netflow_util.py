#!/bin/python3
# Seth Giovanetti


def simple_combine_data(data, sortField):
    return combine_data(data, lambda a, b: a[sortField] == b[sortField], sortField)


def multi_combine_data(data, sortFields):
    return combine_data(data, lambda a, b: all(a[sortField] == b[sortField] for sortField in sortFields), sortFields[0])
    # def e(a, b):
    #     all(a[f] == b[f] for f in sortFields)
    # for sort in sortFields:
    #     data = combine_data(data, e, sort)
    # return data


def combine_data(data, equals, sortField):
    initial_length = len(data)
    # Combines records in data based on the equals function.
    # Only sequential entries after sorting by sortfield will be combined.
    if initial_length is 0:
        print("Warning! Data is empty!")
        return data
    try:
        data_sorted = sorted(data, key=lambda k: k[sortField])
        # print([k[sortField] for k in data_sorted])
    except TypeError:
        print("SortField: " + sortField)
        print("Availible fields: " + str(data[0].keys()))
        print("Bad points: ")
        i = 0
        for point in data:
            if i > 10:
                print("...")
                break
            if point.get(sortField) is None:
                print(point)
                i += 1
        raise
    p = data_sorted.pop()
    groups = []
    group = [p]
    group_sort = p
    while len(data_sorted) is not 0:
        p = data_sorted.pop()
        try:
            if (equals(group_sort, p)):
                group.append(p)
            else:
                groups.append(group)
                group = [p]
                group_sort = p
        except TypeError:
            print("Group_sort:")
            print(group_sort)
            print("New pop:")
            print(p)
            raise
    groups.append(group)
    finaldata = []
    for l in groups:
        combined = {}
        for key in l[0].keys():
            value = 0
            for entry in l:
                try:
                    value += entry[key]
                except TypeError:
                    value = entry[key]
                    break
            combined[key] = value
        finaldata.append(combined)
    print("Consolidated data from " +
          str(initial_length) + " to " + str(len(finaldata)))
    return finaldata


def compress_bytes(data, compress_size):
    for point in data:
        point['bytes_in'] = point['bytes_in'] / compress_size


def localize_bytes(size):
    return "bytes x" + str(size)


def represent_poly(p, var_string='x'):
    res = ''
    first_pow = len(p) - 1
    for i, coef in enumerate(p):
        power = first_pow - i

        if coef:
            if coef < 0:
                sign, coef = (' - ' if res else '- '), -coef
            elif coef > 0:  # must be true
                sign = (' + ' if res else '')

            str_coef = '' if coef == 1 and power != 0 else str(coef)

            if power == 0:
                str_power = ''
            elif power == 1:
                str_power = var_string
            else:
                str_power = var_string + '^' + str(power)

            res += sign + str_coef + str_power
    return res


def top_percent(predata, percent, field):
    totalrecords = len(predata)

    # Calculate total.
    totalvalue = 0
    for point in predata:
        point['bytes_in'] = int(point['bytes_in'])
        totalvalue += point['bytes_in']

    # Get top 10 records by bytes_in
    # Sorts the list by field (bytes_in), gets the #n... #2, #1 entries.
    predata = sorted(predata, key=lambda k: k[field])

    # Initialize array for the final data points
    data = []
    # Map included/total ratio while adding
    included = 0

    # Calculate top % of data, and use that as the data we graph
    # Until the amount of data we have exceeds %[percent], move a data point into our final list.
    while len(predata) > 0 and included < totalvalue * (percent / 100):
        newrecord = predata.pop()
        included += newrecord[field]
        data.append(newrecord)
    print("Records included: " + str(len(data)) + '/' + str(totalrecords))
    return data


def sluggify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    r = value.replace("..\\", "prev")
    r = r.replace("\"", "").replace(" ", "_")
    r = r.replace("\\", "_").replace("/", "_")
    r = r.replace("*", "+").replace("%", "perc")
    return r
