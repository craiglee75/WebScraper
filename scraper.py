#  Web Scraper Project
import string
import requests
import os

from bs4 import BeautifulSoup

url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
pages = int(input('# Pages: '))
news_type = input('News Type?: ')

for i in range(1, pages + 1):
    # create folders for each page
    home = os.getcwd()
    folder = f'Page_{i}'
    path = os.path.join(home, folder)
    print(path)
    os.mkdir(path)
    os.chdir(path)

    # goto each page and search for articles
    url_page = f'&page={i}'
    response = requests.get(url+url_page)
    url_code = response.status_code
    soup = BeautifulSoup(response.content, 'html.parser')

    news_article_links = soup.find_all('span', {'class': 'c-meta__type'}, text={news_type})

    saved_links = []
    saved_titles = []

    # COde finds articles on the page related to the input news type
    for news_article in news_article_links:
        anchor = news_article.find_parent('article').find('a', {'data-track-action': 'view article'})
        saved_links.append(anchor.get('href'))

    # for each article found the code enters the link and grabs the article text
    for link in saved_links:
        article_response = requests.get('https://www.nature.com' + link)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')

        title = article_soup.find('title').text.strip()
        # saved_titles.append(news_type + '_' + title)  # Tagged with news type
        saved_titles.append(title)

        # Finally, removes punctuation and saves article body as type + title + .txt
        for header in saved_titles:
            table = str.maketrans(dict.fromkeys(string.punctuation))
            result = ("".join(header.translate(table))).replace(' ', '_') + '.txt'
            article_body = article_soup.find('div', {'class': "c-article-body"}).text.strip()

            file = open(result, 'w', encoding="UTF-8")
            file.write(article_body)
            file.close()

    # return to original directory before loop begins again.
    os.chdir(home)
