"""
Iter Bus

An example of incremental XML parsing with the ElementTree library

"""

from xml.etree.cElementTree import iterparse

if __name__ == '__main__':
    for event, element in iterparse("tiny_routes.xml", ('start', 'end')):
        if event == 'start' and element.tag == 'buses':
            buses = element
        elif event == 'end' and element.tag == 'bus':
            busdict = dict((child.tag, child.text) for child in element)
            print("%(id)s,%(route)s,%(direction)s,%(latitude)s,%(longitude)s" % busdict)
