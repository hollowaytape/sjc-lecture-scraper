import scrapy


class ItemSpider(scrapy.Spider):
    name = "items"
    start_urls = [
            'http://digitalarchives.sjc.edu/items/browse',
            #'http://digitalarchives.sjc.edu/items/show/2042',
            #'http://digitalarchives.sjc.edu/items/browse?tags=Friday+night+lecture&page=2',
        ]

    def parse(self, response):
        # Follow links to lecture pages
        for href in response.css('div.hentry h2 a::attr(href)'):
            yield response.follow(href, self.parse_lecture)
        # Follow pagination links
        next_page = response.css('li.pagination_next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_lecture(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        id_number = response.url.split("/")[-1]

        result =  {
            'id': id_number,
            'title': extract_with_css('div#content h1::text'),
            'author': extract_with_css('div#dublin-core-creator div.element-text a::text'),
            'date': extract_with_css('div#dublin-core-date div.element-text::text'),
            'location': extract_with_css('div#dublin-core-coverage div.element-text::text'),
            #'subject':  extract_with_css('div#dublin-core-subject div.element-text a::text'),
            'description': extract_with_css('div#dublin-core-description div.element-text::text'),
            'audio_link': extract_with_css('audio#html5-media-1::attr(src)'),
            #'duration': extract_with_css('div#sound-item-type-metadata-duration div.element-text::text'),
            #'duration': extract_with_css('span.mejs-duration::text')    # Loaded with AJAX, doesn't work
        }

        try:
            result['subject'] = extract_with_css('div#dublin-core-subject div.element-text a::text')
        except AttributeError:
            result['subject'] = ''

        try:
            result['duration'] = extract_with_css('div#sound-item-type-metadata-duration div.element-text::text'),
        except AttributeError:
            result['duration'] = ''       # Usually a pretty good guess

        yield result