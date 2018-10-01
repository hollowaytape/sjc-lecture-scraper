import jsonlines
import PyRSS2Gen
import datetime

special_chars = {
    b'\xc3\xa8': b'e',   # e grave
    b'\xc3\xa9': b'e',   # e acute
    b'\xc3\xa4': b'a',   # a umlaut
    b'\xc3\xb6': b'o',    # o umlaut
    b'\xc3\xb8': b'o',   # o umlaut
    b'\xc3\xa6': b'ae',  # ae
    b'\xc4\x81': b'a',   # a bar
    b'\xc5\xab': b'u',   # u bar
    b'\xe1\xb8': b'h',   # h with a thing on the bottom
    b'\xa5\x60': b'a',   # a bar
    b'\xc4\xab': b'i',   # i bar


}

class PodcastRSS(PyRSS2Gen.RSS2):
    rss_attrs = {'xmlns:itunes': "http://www.itunes.com/dtds/podcast-1.0.dtd",
                 'version': '2.0'}

class PodcastItem(PyRSS2Gen.RSSItem):
    # Need to subclass RssItem to add the duration field.
    element_attrs = {}

    def __init__(
        self,
        title=None,
        link=None,
        description=None,
        author=None,
        categories=None,
        comments=None,
        enclosure=None,
        guid=None,
        pubDate=None,
        source=None,
        duration=None
    ):

        if title is None and description is None:
            raise TypeError("Must define at least one of 'title' or 'description'")
        self.title = title
        self.link = link
        self.description = description
        self.author = author
        if categories is None:
            categories = []
        self.categories = categories
        self.comments = comments
        self.enclosure = enclosure
        self.guid = guid
        self.pubDate = pubDate
        self.source = source
        if duration:
            self.duration = duration[0]
        else:
            self.duration = "1:00:00"

    def publish_extensions(self, handler):
        PyRSS2Gen._opt_element(handler, "itunes:duration", self.duration)

parsed_items = []

with jsonlines.open('items.jl') as reader:
    for obj in reader:
        #enclosure = PyRSS2Gen.Enclosure(
        #        url=obj['audio_link'],
        #        length=
        #    )
        if obj['subject']:
            try:
                print(obj['subject'])
            except UnicodeEncodeError:
                obj['subject'] = bytes(obj['subject'], encoding='utf-8')

                for c in special_chars:
                    obj['subject'] = obj['subject'].replace(c, special_chars[c])
                    #print(obj['subject'])

                obj['subject'] = obj['subject'].decode('shift-jis')
                print(obj['subject'])
            description_string = "%s. %s %s." % (obj['subject'], obj['description'], obj['location'])
        else:
            #print("No subject")
            description_string = "%s %s." % (obj['description'], obj['location'])
        item = PodcastItem(
                title=obj['title'],
                link=obj['audio_link'],
                description=description_string,
                guid=obj['id'],
                pubDate=obj['date'],
                duration=obj['duration'],
            )
        parsed_items.append(item)

rss = PodcastRSS(
    title="SJC Friday Night Lectures",
    link="http://digitalarchives.sjc.edu/items/browse?tags=Friday+night+lecture",
    description="Unofficial feed of the recordings of Friday Night Lectures at SJC.",

    lastBuildDate=datetime.datetime.now(),

    image=PyRSS2Gen.Image(
            url='https://diplomaclassics.com/images/Entities/insignia/v2/SjcaSealOrangeGold_220.png',
            title='SJC Logo',
            link='https://diplomaclassics.com/images/Entities/insignia/v2/SjcaSealOrangeGold_220.png',
        ),

    items=parsed_items
    )

rss.write_xml(open("pyrss2gen.xml", "w", encoding='utf-8'))
