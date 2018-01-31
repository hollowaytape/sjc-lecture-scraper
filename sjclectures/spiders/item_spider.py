import scrapy


class ItemSpider(scrapy.Spider):
    name = "items"
    start_urls = [
            'http://digitalarchives.sjc.edu/items/browse',
        ]

    def parse(self, response):
        # Follow links to lecture pages
        for href in response.css('div.hentry h2 a::attr(href)'):
            yield response.follow(href, self.parse_lecture)
        # Follow pagination links
        next_page = response.css('li.pagination_next a::attr(href)').extract_first()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' + next_page)
        if next_page is not None:
            yield response.follow(next_page, self.parse)

        #page = response.url.split("/")[-1]

        #for item in response.css('div.hentry'):
        #    yield {
        #        'title': item.css("h2 a::text").extract_first(),
        #        'link': item.css("h2 a::attr(href)").extract_first(),
        #        'description': item.css("div.item-meta div.item-description::text").extract_first().lstrip('\r\n        '),
        #    }

        #filename = 'items-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)

    def parse_lecture(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'title': extract_with_css('div#content h1::text'),
            'author': extract_with_css('div#dublin-core-creator div.element-text a::text'),
            'date': extract_with_css('div#dublin-core-date div.element-text::text'),
            'audio_link': extract_with_css('audio#html5-media-1::attr(src)'),
            'subject':  extract_with_css('div#dublin-core-subject div.element-text a::text'),
        }