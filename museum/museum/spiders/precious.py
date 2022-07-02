# imports 

import scrapy
from scrapy.loader import ItemLoader
from museum.items import MuseumItem
from scrapy_playwright.page import PageMethod

# header to dictonary
def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []) -> dict():
    d = dict()
    for kv in s.split('\n'):
        kv = kv.strip()
        if kv and sep in kv:
            v=''
            k = kv.split(sep)[0]
            if len(kv.split(sep)) == 1:
                v = ''
            else:
                v = kv.split(sep)[1]
            if v == '\'\'':
                v =''
            # v = kv.split(sep)[1]
            if strip_cookie and k.lower() == 'cookie': continue
            if strip_cl and k.lower() == 'content-length': continue
            if k in strip_headers: continue
            d[k] = v
    return d

class PreciousSpider(scrapy.Spider):
    name = 'project'
    allowed_domains = ['utas.edu.au']
    url = 'https://www.utas.edu.au/research/degrees/available-projects'

# header 

    def start_requests(self):
        h = get_headers(
            '''
            accept: */*
            accept-encoding: gzip, deflate, br
            accept-language: en-US,en;q=0.9
            origin: https://www.utas.edu.au
            referer: https://www.utas.edu.au/
            sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"
            sec-ch-ua-mobile: ?0
            sec-ch-ua-platform: "Windows"
            sec-fetch-dest: empty
            sec-fetch-mode: cors
            sec-fetch-site: cross-site
            user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
            '''
        )
        # playwrigth initialize 

        yield scrapy.Request(self.url, headers =h, meta=dict(
            playwright = True,
            playwright_include_page = True``, # for waiting for a particular element to load 
            errback=self.errback
            
        )) 
        # itemloader

    def parse(self, response):
        for link in response.css('.search-result__card--link.button.button--transparent::attr(href)'): # individual doctor's link
            yield response.follow(link.get(), callback = self.parse_categories) # enter into the website

    def parse_categories(self, response):
        l = ItemLoader(item  = MuseumItem(), selector = response)

        l.add_css('name', '.internal-banner__content--title')
        l.add_css('project_description', 'div#content-start > p')
        l.add_css('primary_supervisor', 'a.button.button--transparent')
        l.add_css('supervisor_email', 'a.button.button--transparent::attr(href)')
        l.add_value('project_link', response.url)
        l.add_xpath('dead_line', '//*[@id="content-start"]/div[1]/div/div[2]/p')

        yield l.load_item()
        # playwright errback at the very last

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()