import jsonlines
import PyRSS2Gen
import datetime

parsed_items = []

with jsonlines.open('items.jl') as reader:
    for obj in reader:
        item = PyRSS2Gen.RSSItem(
                title=obj['title'],
                link=obj['audio_link'],
                description=obj['subject'] + " delivered by " + obj['author'],
                guid=obj['id'],
                pubDate=obj['date'],
            )
        parsed_items.append(item)

rss = PyRSS2Gen.RSS2(
    title="SJC Friday Night Lectures",
    link="http://digitalarchives.sjc.edu/items/browse?tags=Friday+night+lecture",
    description="Unofficial feed of the recordings of Friday Night Lectures at SJC.",

    lastBuildDate=datetime.datetime.now(),

    items=parsed_items
    )

rss.write_xml(open("pyrss2gen.xml", "w", encoding='utf-8'))
