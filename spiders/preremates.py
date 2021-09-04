from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
import unicodedata
import scrapy
import time
from scrapy.crawler import CrawlerProcess



class ElectronicsSpider(scrapy.Spider):
    name = "pre-remates"
    allowed_domains = ["preremates.cl"]
    start_urls = [
        'https://preremates.cl/content/proximos-remates?page=1',
        'https://preremates.cl/content/proximos-remates?page=2',
        'https://preremates.cl/content/proximos-remates?page=3',
        'https://preremates.cl/content/proximos-remates?page=4'
    ]

    def mark(self, text):
        print("="*30)
        print(text)
        print("="*30)

    def parse(self, response):
        self.mark(response.url)
        for detalle in response.css(".row"):
            date = unicodedata.normalize('NFKD', u"\n".join(detalle.css("span.aviso-fecha::text").extract()))
            desc =  unicodedata.normalize('NFKD', u"\n".join(detalle.css("div.aviso-texto::text").extract()))
            if desc.strip() != "":
                yield {"url":str(response.url), "desc": desc, "date":date}

        for link in response.css(".ktkPageLinks a::attr(href)"):
            l = str(link.extract())
            if l.startswith("/content/proximos-remates"):        
                yield response.follow( l, self.parse )

if __name__ == "__main__":
    process = CrawlerProcess({ 'LOG_LEVEL': 'ERROR'})
    process.crawl(ElectronicsSpider)
    process.start()