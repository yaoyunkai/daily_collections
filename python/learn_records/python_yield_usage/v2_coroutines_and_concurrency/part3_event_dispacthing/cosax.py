import xml.sax
from xml.sax import ContentHandler

from coroutine import coroutine


class EventHandler(ContentHandler):
    def __init__(self, target):
        self.target = target

    def startElement(self, name, attrs):
        self.target.send(('start', (name, attrs._attrs)))

    def characters(self, text):
        self.target.send(('text', text))

    def endElement(self, name):
        self.target.send(('end', name))


@coroutine
def printer():
    while True:
        event = (yield)
        print(event)


if __name__ == '__main__':
    xml.sax.parse("tiny_routes.xml", EventHandler(printer()))
