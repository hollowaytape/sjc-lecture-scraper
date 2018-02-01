import jsonlines
import PyRSS2Gen
import datetime

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
        self.duration = duration

    def publish_extensions(self, handler):
        PyRSS2Gen._opt_element(handler, "itunes:duration", self.duration)

parsed_items = []

with jsonlines.open('items.jl') as reader:
    for obj in reader:
        #enclosure = PyRSS2Gen.Enclosure(
        #        url=obj['audio_link'],
        #        length=
        #    )
        item = PodcastItem(
                title=obj['title'],
                link=obj['audio_link'],
                description="%s. %s %s." % (obj['subject'], obj['description'], obj['location']),
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
