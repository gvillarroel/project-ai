import unicodedata
from numpy import extract
import scrapy
import time
import logging
import re
import json
import pandas as pd
import os
logger = logging.getLogger()
import re

class ElectronicsSpider(scrapy.Spider):
    name = "economicos"
    allowed_domains = ["www.economicos.cl"]
    start_urls = [
        'https://www.economicos.cl/todo_chile/propiedades'
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        try:
            self.memory = pd.read_json(open(f"data/{self.name}_memory.json"))
        except:
            self.memory = pd.DataFrame.from_dict({"url": ["https://www.yapo.cl/chile/comprar?ca=12_s&l=0"]})
        print(self.memory.head())
    def parse(self, response):
        time.sleep(1)
        print(f"Processing {response.url}")
        detalles = response.css("#detalle")
        got_link = False
        for link in response.css("a::attr(href)"):
            l = str(link.extract())
            if l.startswith("/propiedades") or "propiedades?" in l:
                if not detalles and self.memory[self.memory.url.str.contains(l) ].count()[0] == 0:
                    got_link = True
                    if l.startswith("/propiedades"):
                        self.memory = self.memory.append({"url": l}, ignore_index=True)
                    yield response.follow( l, self.parse )
        for detalle in detalles:
            data = {
                "url": response.url,
                "description": unicodedata.normalize('NFKD', u" ".join(detalle.css("#description p::text").extract())),
                "price": " ".join(map(str.strip, detalle.css("div.cont_price_detalle_f::text").extract()))
                }
            data = {**data, **dict([(" ".join(d.css("span::text").extract()), " ".join(map(str.strip, d.css("li::text").extract()),)) for d in detalle.css("#specs li")])}
            yield data
        if not detalles and not got_link:
            self.crawler.engine.close_spider(self, "nothing to do")
    def close(self, reason):
        print(f"close reason:{reason}")
        self.memory.to_json(f"data/{self.name}_memory.json")