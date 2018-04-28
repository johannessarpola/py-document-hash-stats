from operator import itemgetter,attrgetter
from itertools import groupby


def group_by_field(data, field):
    data.sort(key=itemgetter(field))
    result = {}
    for f, items in groupby(data, key=itemgetter(field)):
        result[str(f)] = items
    return result

def group_by_attribute(data, attribute):
    get_attr = attrgetter(attribute)
    data.sort(key=get_attr)
    result = {k: list(g) for k, g in groupby(data, get_attr)}
    return result