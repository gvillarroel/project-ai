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
        'http://preremates.cl/content/proximos-remates'
    ]

    def mark(self, text):
        print("="*30)
        print(text)
        print("="*30)

    def parse(self, response):
        self.mark(response.url)
        for detalle in response.css(".row"):
            date = str( unicodedata.normalize('NFKD', u"\n".join(detalle.css("span.aviso-fecha::text").extract())).encode("iso-8859-15",'ignore') )
            desc = str( unicodedata.normalize('NFKD', u"\n".join(detalle.css("div.aviso-texto::text").extract())).encode("iso-8859-15",'ignore'))
            yield {"url":str(response.url), "desc": desc, "date":date}

        for link in response.css(".ktkPageLinks a::attr(href)"):
            l = str(link.extract())
            if l.startswith("/content/proximos-remates"):        
                yield response.follow( l, self.parse )

if __name__ == "__main__":
    process = CrawlerProcess({ 'LOG_LEVEL': 'ERROR'})
    process.crawl(ElectronicsSpider)
    process.start()