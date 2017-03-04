import scrapy


class AffiliateSpider(scrapy.Spider):
    name = "affiliate"

    def start_requests(self):
        main_url = 'http://games.crossfit.com/affiliate/'
        max_affiliates = 2

        for id in (663, 18921, 10000, 16000, 1, 18922):
            url = main_url + str(id)
            yield scrapy.Request(url=url, callback=self.parse,
                                 errback=self.err_handler)

    def err_handler(self, response):
        pass

    def parse(self, response):
        # Getting affiliate id
        affiliate_id = response.url.split("/")[-1]

        # Getting affiliate name
        fname_selector = response.css('h3.c-heading-page-cover small::text')
        lname_selector = response.css('h3.c-heading-page-cover::text')

        first_name = fname_selector.extract()[0]
        last_name = lname_selector.re(r'\w+')[0]

        affiliate_name = first_name + ' ' + last_name

        # Getting affiliate info:
        # (Country, Region, Location)
        labels = ['Country']
        labels += response.css('div.item-label::text').re(r'\w+')[:2]

        items = list(map(str.strip,
                         response.css('div.text small::text').extract()))
        items += map(str.strip,
                     response.css('div.text::text').extract()[2: 5: 2])

        self.log(f"Affiliate ({affiliate_name}) -> ID ({affiliate_id})")

        for l, i in zip(labels, items):
            yield self.log(f"{l} -> {i}")
