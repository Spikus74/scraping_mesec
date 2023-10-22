import requests
from bs4 import BeautifulSoup

url = "https://www.uctovani.net/clanky.php"
received = requests.get(url)
soup = BeautifulSoup(received.text,"html.parser")

found = soup.find_all("h3",class_="title")
elem = [x.find("a") for x in found]
links = [link.get("href") for link in elem]
#print(links)
titles = [x.get_text() for x in elem]
final = [(title,link) for title,link in zip(titles,links)]
print(final)