import xml.sax


class MyHandler(xml.sax.ContentHandler):
    def startElement(self, name, attrs):
        print(f'start element: {name}')

    def endElement(self, name):
        print(f'end element: {name}')

    def characters(self, content):
        print(f'characters: {repr(content)[:40]}')


if __name__ == '__main__':
    xml.sax.parse('allroutes.xml', MyHandler())
