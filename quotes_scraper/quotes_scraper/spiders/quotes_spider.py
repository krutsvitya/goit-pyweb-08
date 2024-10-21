import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']

    custom_settings = {
        'FEEDS': {
            'quotes.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 4,
                'overwrite': True,
            },
        }
    }

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract_first(),
                "quote": quote.xpath("span[@class='text']/text()").get(),
            }

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=response.urljoin(next_link), callback=self.parse)


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    start_urls = ['http://quotes.toscrape.com']

    custom_settings = {
        'FEEDS': {
            'authors.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 4,
                'overwrite': True,
            },
        }
    }

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            author_url = quote.xpath("span/a/@href").get()
            yield response.follow(author_url, self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=response.urljoin(next_link), callback=self.parse)

    def parse_author(self, response):
        name = response.xpath("//h3[@class='author-title']/text()").get().strip()
        birthdate = response.xpath("//span[@class='author-born-date']/text()").get()
        birthplace = response.xpath("//span[@class='author-born-location']/text()").get().strip()
        description = response.xpath("//div[@class='author-description']/text()").get().strip()

        yield {
            'name': name,
            'birthdate': birthdate,
            'birthplace': birthplace,
            'description': description,
        }

