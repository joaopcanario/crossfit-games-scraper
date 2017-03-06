from collections import namedtuple

import scrapy


class AthleteSpider(scrapy.Spider):
    name = "athlete"

    Athlete = namedtuple('Athlete', ['id', 'name', 'region', 'division',
                                     'age', 'height', 'weight', 'affiliate',
                                     'team'])
    Athlete.__new__.__defaults__ = (None,) * len(Athlete._fields)

    def start_requests(self):
        max_athletes = 1103044

        for id in range(1, max_athletes):
            url = f'http://games.crossfit.com/athlete/str(id)'
            yield scrapy.Request(url=url, callback=self.parse,
                                 errback=self.err_handler)

    def err_handler(self, response):
        pass

    def parse(self, response):
        # Getting athlete id
        athlete = self.Athlete(id=response.url.split("/")[-1])

        # Getting athlete name
        fname_selector = response.css('h3.c-heading-page-cover small::text')
        lname_selector = response.css('h3.c-heading-page-cover::text')

        first_name = fname_selector.extract()[0]
        last_name = lname_selector.re(r'\w+')[0]

        athlete = athlete._replace(name=f'{first_name} {last_name}')

        # Getting athlete info:
        # (Region, Division, Age, Height, Weight, Affiliate, Team)
        labels = list(map(str.lower,
                          response.css('div.item-label::text').re(r'\w+')))

        items = response.css('div.text::text').re(r'\w+.*\w*') + \
                response.css('div.text a::text').extract()

        athlete = athlete._replace(**dict(zip(labels, items)))

        self.log(f"{athlete}")
