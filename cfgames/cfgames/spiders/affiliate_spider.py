from collections import namedtuple

import scrapy


class AffiliateSpider(scrapy.Spider):
    name = "affiliate"

    Affiliate = namedtuple('Affiliate', ['id', 'name', 'country', 'region',
                                         'city', 'state'])
    Affiliate.__new__.__defaults__ = (None,) * len(Affiliate._fields)

    def start_requests(self):
        max_affiliates = 20000

        for id in range(1, max_affiliates):
            url = f'http://games.crossfit.com/affiliate/{str(id)}'
            yield scrapy.Request(url=url, callback=self.parse,
                                 errback=self.err_handler)

    def err_handler(self, response):
        pass

    def parse(self, response):
        # Creating affiliate id
        affiliate = self.Affiliate(id=response.url.split("/")[-1])

        # Getting affiliate name
        fname_selector = response.css('h3.c-heading-page-cover small::text')
        lname_selector = response.css('h3.c-heading-page-cover::text')

        first_name = fname_selector.extract()[0]
        last_name = lname_selector.re(r'\w+')[0]

        affiliate = affiliate._replace(name=f'{first_name} {last_name}')

        # Getting affiliate info:
        # (Country, Region, Location)
        items = list(map(str.strip,
                         response.css('div.text small::text').extract()))
        items += map(str.strip,
                     response.css('div.text::text').extract()[2: 5: 2])

        affiliate = affiliate._replace(country=items[0],
                                       region=items[1],
                                       city=items[2].split(',')[0].strip(),
                                       state=items[2].split(',')[1].strip())

        if affiliate.country == 'Brazil' and affiliate.state == 'Bahia':
            yield affiliate._asdict()