from requests import get
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor


@dataclass
class Article:
    url: str
    title: str
    content: str
    image_url: str = None
    
    def dict(self):
        return asdict(self)


class NewsParser:
    
    def __init__(self, base_url, path):
        self.base_url = base_url
        self.path = path
        self.page = f"https://{base_url}{path}"
        
    def parse(self):
        response = get(self.page)
        if response.status_code != 200:
            raise Exception(f'The page {URL} is not accessable!')

        articles = []
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        top_news_tag = soup.find('div', {'class': 'short-top'})

        for a_tag in top_news_tag:
            link = a_tag['href']
            if not link.startswith('https'):
                link = f"https://{self.base_url}{link}"
            title = a_tag.span.string.strip()
            articles.append(Article(link, title, None, None))

        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.__process_articles, articles)

        return articles

    def __process_articles(self, article):
        response = get(article.url)
        if response.status_code != 200:
            raise Exception(f'The page {article.link} is not accessable!')

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        article_text = soup.find('div', {'class': 'article-text'})
        if article_text is None:
            article_text = soup.find(id='opennewstext')
            p_tags = article_text.find_all('p')[1:]
        else:
            p_tags = article_text.span.find_all('p')

        words = []
        for p_tag in p_tags:
            words.extend(p_tag.text.split())
            if len(words) > 50:
                words[50:] = ['...']
                break
        article.content = ' '.join(words)

        image_path = article_text.img['src'].strip('/')
        if not image_path.endswith('logo.png'):
            sub_domain = article.url.split(self.base_url)[0]
            article.image_url = f"{sub_domain}{self.base_url}/{image_path}"
