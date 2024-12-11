"""
cosax.py

An example showing how to push SAX events into a coroutine target

start: tag开始的匹配
text: text之后的文字
end: tag结束

text: 两个tag之间的空白

start: tag开始的匹配
text: text之后的文字
end: tag结束


"""

import xml
from xml.sax.handler import ContentHandler


class EventHandler(ContentHandler):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def startElement(self, name, attrs):
        self.target.send(('start', (name, attrs._attrs)))

    def characters(self, text):
        self.target.send(('text', text))

    def endElement(self, name):
        self.target.send(('end', name))


# example use
if __name__ == '__main__':
    def coroutine(func):
        def start(*args, **kwargs):
            cr = func(*args, **kwargs)
            cr.send(None)
            return cr

        return start


    @coroutine
    def printer():
        while True:
            event = (yield)
            print(event)


    xml.sax.parse("allroutes.xml", EventHandler(printer()))
