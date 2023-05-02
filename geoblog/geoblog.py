from pelican import signals
from xml.dom import minidom

settings = {}
collection = {}
gpx_root = '''<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="nfc.flux.vision"></gpx>'''
kml_root = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2"><Document><Folder></Folder></Document></kml>'''

def init(self):
    settings['files'] = self.settings.get('OUTPUT_PATH')

def generate_latlon(generator):
    for article in generator.articles:
        if "location" in article.metadata:
            lat, lon = [float(i) for i in article.metadata['location'].replace(' ', '').split(',')]
            article.metadata['lat'] = lat
            article.metadata['lon'] = lon

def make_files(void):
    print(collection)
    makeGPX()
    makeKML()

def makeKML():
    if len(collection) > 0:
        root = minidom.parseString(kml_root)
        folder = root.createElement('name')
        foldername = root.createTextNode( 'articles' )
        folder.appendChild( foldername )
        root.childNodes[0].childNodes[0].childNodes[0].appendChild( folder )
        for place in collection:
            placemark = root.createElement('Placemark')
            name = root.createElement('name')
            title = root.createTextNode( collection[place]['name'] + ' (' + collection[place]['url'] +')')
            name.appendChild( title )
            placemark.appendChild( name )
            point = root.createElement('Point')
            coordinates = root.createElement('coordinates')
            lat, lon = collection[place]['coordinates'].replace(' ', '').split(',')
            latlon = root.createTextNode( lon + ',' + lat)
            coordinates.appendChild( latlon )
            point.appendChild( coordinates )
            placemark.appendChild( point )
            root.childNodes[0].childNodes[0].childNodes[0].appendChild( placemark )
        with open(settings['files'] + '/articles.kml', 'w') as xml_file:
            root.writexml(xml_file, indent="", addindent="  ", newl='\n')

def makeGPX():
    if len(collection) > 0:
        root = minidom.parseString(kml_root)
        for place in collection:
            lat, lon = collection[place]['coordinates'].replace(' ', '').split(',')
            wpt = root.createElement('wpt')
            wpt.setAttribute('lat', lat)
            wpt.setAttribute('lon', lon)
            name = root.createElement('name')
            title = root.createTextNode( collection[place]['name'] + ' (' + collection[place]['url'] +')' )
            name.appendChild( title )
            wpt.appendChild( name )
            root.childNodes[0].appendChild( wpt )
        with open(settings['files'] + '/articles.gpx', 'w') as xml_file:
            root.writexml(xml_file, indent="", addindent="  ", newl='\n')

def geodata(generator):
    for article in generator.articles:
        if "location" in article.metadata:
            collection.update({
                article.slug : {
                    "url" : generator.settings['SITEURL'] + '/' + article.url,
                    "name": article.title,
                    "coordinates": article.metadata["location"],
                }
            })

def register():
    signals.initialized.connect(init)
    signals.article_generator_finalized.connect(generate_latlon)
    signals.article_generator_finalized.connect(geodata)
    signals.finalized.connect(make_files)