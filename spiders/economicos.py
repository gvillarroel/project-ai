import unicodedata
import scrapy
import time

class ElectronicsSpider(scrapy.Spider):
    name = "electronics"
    allowed_domains = ["www.economicos.cl"]
    start_urls = [
        'https://www.economicos.cl/todo_chile/remates_de_propiedades_el_mercurio'
    ]

    def parse(self, response):
        time.sleep(2)
        for link in response.css("a::attr(href)"):
            l = str(link.extract())
            if l.startswith("/todo_chile/remates_de_propiedades_el_mercurio")\
                    or l.startswith("/remates/"):
                yield response.follow( l, self.parse )
        for detalle in response.css("#detalle"):
            desc = unicodedata.normalize('NFKD', u"\n".join(detalle.css("#description p::text").extract()))
            date = u"\n".join([d for d in detalle.css("#specs li::text").extract()])
            yield {"url":str(response.url), "desc": desc, "date":date}