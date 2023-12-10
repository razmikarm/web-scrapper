from requests import get
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor


@dataclass
class Article:
    link: str
    title: str
    content: str
    image_url: str = None
    
    def dict(self):
        return asdict(self)


class NewsParser:
    
    def __init__(self, base_url, path):
        self.base_url = base_url
        self.path = path
        self.page = f"{base_url}{path}"
        
    def parse(self):
        response = get(self.page)
        if response.status_code != 200:
            raise Exception(f'The page {URL} is not accessable!')

        articles = []
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        top_news_tag = soup.find('div', {'class': 'short-top'})

        for a_tag in top_news_tag:
            link = f"{self.base_url}{a_tag['href']}"
            title = a_tag.span.string.strip()
            articles.append(Article(link, title, None, None))

        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.__process_articles, articles)

        return articles

    def __process_articles(self, article):
        response = get(article.link)
        if response.status_code != 200:
            raise Exception(f'The page {article.link} is not accessable!')

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        article_text = soup.find('div', {'class': 'article-text'})
        
        p_tags = article_text.span.find_all('p')
        content = ''.join([p_tag.text for p_tag in p_tags])
        article.content = f"{content[:50]}..." if len(content) > 50 else content

        image_path = article_text.img['src']
        if image_path.endswith('default.jpg'):
            image_url = f"{self.base_url}/{image_path}"
