import requests
from bs4 import BeautifulSoup
from unidecode import unidecode


url = "https://www.businessinfo.cz/"
request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")
links = [link.get("href") for link in soup.find_all("a", href=True)]
filtered_links = [link for link in links if "businessinfo.cz/clanky/" in link]
final_links = filtered_links[2:]

title = soup.find_all("span",class_="title-text")
for x in title:
    nex = unidecode(x)
    title[title.index(x)] = nex
pretitles = [t.text for t in title]
final_titles = [x.encode("latin1").decode("utf-8") for x in pretitles]
final = [(title,link) for title,link in zip(final_titles,final_links)]
print(final)
