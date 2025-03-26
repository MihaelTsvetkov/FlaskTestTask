import xml.sax as xs
from xml.sax.xmlreader import AttributesImpl


class TagCounterHandler(xs.ContentHandler):
    def __init__(self, target_tag: str) -> None:
        self.target_tag: str = target_tag
        self.count: int = 0

    def startElement(self, name: str, attrs: AttributesImpl) -> None:
        if name == self.target_tag:
            self.count += 1
