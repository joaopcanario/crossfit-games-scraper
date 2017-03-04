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
        # Getting athlete id
        athlete_id = response.url.split("/")[-1]

        # Getting athlete name
        fname_selector = response.css('h3.c-heading-page-cover small::text')
        lname_selector = response.css('h3.c-heading-page-cover::text')

        first_name = fname_selector.extract()[0]
        last_name = lname_selector.re(r'\w+')[0]

        athlete_name = first_name + ' ' + last_name

        # Getting athlete info:
        # (Region, Division, Age, Height, Weight, Affliate, Team)
        labels = response.css('div.item-label::text').re(r'\w+')

        items = response.css('div.text::text').re(r'\w+.*\w*') + \
                response.css('div.text a::text').extract()

        self.log(f"Info of Athlete ({athlete_name}) -> ID ({athlete_id})")

        for l, i in zip(labels, items):
            yield self.log(f"{l} -> {i}")
