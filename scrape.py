import requests
from bs4 import BeautifulSoup  # you could use scrapy framework
import pprint
import sys

try:
    page = sys.argv[1]
except IndexError:
    print('What page do you wanna see with the 1st one? If none, write 1 after script.py')
    sys.exit(1)
# this func requests page from hackernews and gets links and subtext(for score)


def get_pages(pagef=1):
    res = requests.get('https://news.ycombinator.com/news?p={}'.format(pagef))
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.storylink')
    subtext = soup.select('.subtext')
    return links, subtext

# this func(below) combines default page and page that you asked with sys.argv


def two_and_more():
    links, subtext = get_pages()
    links2, subtext2 = get_pages(page)
    sumlinks = links + links2
    sumsubtext = subtext + subtext2
    return sumlinks, sumsubtext

# sorts articles by votes (more or equal 100)


def sort_articles_by_votes(site_info_list):
    return sorted(site_info_list, key=lambda k: k['vote'], reverse=True)


def create_custom_hn():
    links, subtext = two_and_more()
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100:
                hn.append({'title': title, 'link': href, 'vote': points})
    return sort_articles_by_votes(hn)


pprint.pprint(create_custom_hn())
