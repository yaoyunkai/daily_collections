# buses.py
#
# An example of setting up an event handling pipeline with coroutines
# and XML parsing.

import xml.sax

from coroutine import coroutine


@coroutine
def buses_to_dicts(target):
    while True:
        event, value = yield

        # look for bus element
        if event == 'start' and value[0] == 'bus':
            busdict = {}
            fragments = []

            # capture text from inner elements
            # end event, tag name from value
            while True:
                event, value = yield
                if event == 'start':
                    fragments = []
                elif event == 'text':
                    fragments.append(value)
                elif event == 'end':
                    if value != 'bus':
                        busdict[value] = ''.join(fragments)
                    else:
                        target.send(busdict)
                        break


@coroutine
def filter_on_field(fieldname, value, target):
    while True:
        d = yield
        if d.get(fieldname) == value:
            target.send(d)


@coroutine
def bus_locations():
    while True:
        bus = yield
        print("%(route)s,%(id)s,%(direction)s,%(latitude)s,%(longitude)s" % bus)


if __name__ == '__main__':
    import xml.sax
    from cosax import EventHandler

    d1 = buses_to_dicts(bus_locations())
    d2 = buses_to_dicts(filter_on_field('direction', 'North Bound', bus_locations()))

    xml.sax.parse('tiny_routes.xml', EventHandler(d2))
