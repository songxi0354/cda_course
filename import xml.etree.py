import xml.etree.ElementTree as ET

tree = ET.parse('/Volumes/1TB/Cursor_Profile_2/pdf.opml')
root = tree.getroot()

def parse_outline(outline, level=1):
    text = outline.attrib.get('text', '')
    if text:
        print('#' * level + ' ' + text)
    for child in outline.findall('outline'):
        parse_outline(child, level+1)

for o in root.findall('./body/outline'):
    parse_outline(o)