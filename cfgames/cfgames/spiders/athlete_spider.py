import scrapy


class AthleteSpider(scrapy.Spider):
    name = "athlete"

    def start_requests(self):
        main_url = 'http://games.crossfit.com/athlete/'
        max_athletes = 1103044

        for id in range(1, max_athletes):
            url = main_url + str(id)
            yield scrapy.Request(url=url, callback=self.parse,
                                 errback=self.err_handler)

    def err_handler(self, response):
        pass

    def parse(self, response):
        athlete_id = response.url.split("/")[-1]

        name_selector = response.css('h3.c-heading-page-cover small::text')

        first_name = name_selector.extract()[0]
        last_name = name_selector.re(r'\w+')[0]

        athlete_name = first_name + ' ' + last_name

        labels = response.css('div.item-label::text').re(r'\w+')

        items = response.css('div.text::text').re(r'\w+.*\w*') + \
                response.css('div.text a::text').extract()

        self.log(f"Info of Athlete ({athlete_name}) -> ID ({athlete_id})")

        for l, i in zip(labels, items):
            yield self.log(f"{l} -> {i}")
