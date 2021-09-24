# project-ai

## Spiders

Ejecutar spider
```bash
scrapy runspider spiders/preremates.py -O data/preremates.json --loglevel=ERROR

scrapy runspider spiders/economicos.py -O data/economicos.json --loglevel=ERROR


scrapy runspider spiders/yapo.py -O data/yapo.json --loglevel=ERROR

scrapy runspider spiders/yapo_chile.py -O data/yapo_chile.json --loglevel=ERROR
Get-Content .\yapo_chile.json -Tail 1
Select-String -path .\yapo_chile.json -pattern "PATIO, 2 ESTACIONAMIENTOS y 1 BODEGA muy amplios."
Get-ChildItem data/economicos.json
```