import requests
from bs4 import BeautifulSoup
import scraping_mesec.py


url = "https://www.podnikatel.cz"
result = requests.get(url)
soup = BeautifulSoup(result.text,"html.parser")

found = soup.find_all("a", class_="design-article__heading design-article__link--major design-article__link--default design-article__link")
final = list()
links = [x.get("href") for x in found]
found2 = soup.find_all("h3",class_="element-heading-reset")
titles = [x.text[1:-1] for x in found2]
for x in links:
    newlink = url+x
    index = links.index(x)
    links[index] = newlink
for title,link in zip(titles,links):
    clean_string = title.replace('\xa0', ' ')
    final.append((clean_string,link))

print(scraping_mesec.funcs.display_article(articles=final,num=0))


