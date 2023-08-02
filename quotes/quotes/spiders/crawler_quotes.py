from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


#TODO: not parse, delete quotes "Від імені автора"

class BaseCrawler(CrawlSpider):
    allowed_domains = ["tsytaty.com"]

    rules = (
        Rule(LinkExtractor(allow="page"), follow=True, callback="parse_all"),
    )

    def parse_quotes(self, quote):
        
    
        text = quote.css(".text > blockquote::text").getall()
        author = quote.css(".text > blockquote > footer > cite > a::text").getall()
        category = quote.css(".category > a::text").getall()

        return {
            "text": text,
            "author": author,
            "category": category
        }


class All_Quotes(BaseCrawler):
    name = "All_Quotes"
    start_urls = ["https://tsytaty.com/"]

    def parse_all(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class Books(BaseCrawler):
    name = "Books"
    start_urls = ["https://tsytaty.com/z-knyh/"]

    def parse_books(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class Movies(BaseCrawler):
    name = "Movies"
    start_urls = ["https://tsytaty.com/z-filmiv/"]

    def parse_movies(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class famousPeople(BaseCrawler):
    name = "famousPeople"
    start_urls = ["https://tsytaty.com/vidomykh-ludei/"]

    def parse_famousPeople(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class Life(BaseCrawler):
    name = "Life"
    start_urls = ["https://tsytaty.com/pro-zhyttya/"]


    def parse_Life(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class Happiness(BaseCrawler):
    name = "Happiness"
    start_urls = ["https://tsytaty.com/pro-shchastya/"]


    def parse_Happiness(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class Love(BaseCrawler):
    name = "Love"
    start_urls = ["https://tsytaty.com/pro-lyubov/"]


    def parse_Love(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class Friendship(BaseCrawler):
    name = "Friendship"
    start_urls = ["https://tsytaty.com/pro-druzhbu/"]


    def parse_Friendship(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class Motivations(BaseCrawler):
    name = "Motivations"
    start_urls = ["https://tsytaty.com/motyvazia/"]


    def parse_Motivations(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class Art(BaseCrawler):
    name = "Art"
    start_urls = ["https://tsytaty.com/motyvazia/pro-tvorchist/"]


    def parse_Art(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class Sport(BaseCrawler):
    name = "Sport"
    start_urls = ["https://tsytaty.com/motyvazia/pro-sport/"]


    def parse_Sport(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class FaithInMyself(BaseCrawler):
    name = "FaithInMyself"
    start_urls = ["https://tsytaty.com/motyvazia/pro-viru-v-sebe/"]


    def parse_FaithInMyself(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class SuccessAndSuccess(BaseCrawler):
    name = "SuccessAndSuccess"
    start_urls = ["https://tsytaty.com/motyvazia/pro-uspih/"]


    def parse_SuccessAndSuccess(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class Season(BaseCrawler):
    name = "_Season"
    start_urls = ["https://tsytaty.com/pro-pory-roku/"]


    def parse_Season(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)


class School(BaseCrawler):
    name = "Season"
    start_urls = ["https://tsytaty.com/shkola/"]


    def parse_School(self, response):
        quotes = response.css(".box_in")
        
        for quote in quotes:
            yield self.parse_quotes(quote)