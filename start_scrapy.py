import os
from scrapy.crawler import CrawlerProcess
from quotes.quotes.spiders.crawler_quotes import All_Quotes


# path directory save result 
output_dir = 'results_scrapy'
os.makedirs(output_dir, exist_ok=True)


# launch process 
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': os.path.join(output_dir, 'quotes.json'),
    'FEED_EXPORT_ENCODING': 'utf-8', 
})


process.crawl(All_Quotes)
process.start() 