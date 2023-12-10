from parser import NewsParser
from pprint import pprint

parser = NewsParser(
    base_url='https://news.am',
    path='/eng/'
)

pprint([report.dict() for report in parser.parse()])
