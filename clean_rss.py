"""
	Pretty-print pyrss2gen's outputted XML, then save it in lecturefeed.rss.
"""

import lxml.etree as etree

x = etree.parse("pyrss2gen.xml")
output = etree.tostring(x, xml_declaration=True, encoding='utf-8', pretty_print=True)
# Gotta change the encoding
#output.replace(b'<?xml version="1.0" ?>', b'<?xml version="1.0" encoding="utf-8">')
with open('lecturefeed.rss', 'wb') as f:
	f.write(output + b'</xml>')