"""


Created at 2023/4/4
"""


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.send(None)
        return cr

    return start


@coroutine
def buses_to_dicts(target):
    """
    状态机程序

    """

    while True:
        event, value = (yield)
        # Look for the start of a <bus> element
        if event == 'start' and value[0] == 'bus':
            busdict = {}
            fragments = []
            # Capture text of inner elements in a dict
            while True:
                event, value = (yield)
                if event == 'start':
                    fragments = []
                elif event == 'text':
                    fragments.append(value)
                elif event == 'end':
                    if value != 'bus':
                        busdict[value] = "".join(fragments)
                    else:
                        target.send(busdict)
                        break


@coroutine
def filter_on_field(field_name, value, target):
    while True:
        d = (yield)
        if d.get(field_name) == value:
            target.send(d)


@coroutine
def bus_locations():
    while True:
        bus = (yield)
        print("%(route)s,%(id)s,\"%(direction)s\", %(latitude)s,%(longitude)s" % bus)


# Example
if __name__ == '__main__':
    import xml.sax
    from cosax import EventHandler

    xml.sax.parse("allroutes.xml",
                  EventHandler(
                      buses_to_dicts(
                          filter_on_field("route", "22",
                                          filter_on_field("direction", "North Bound",
                                                          bus_locations())))
                  ))
