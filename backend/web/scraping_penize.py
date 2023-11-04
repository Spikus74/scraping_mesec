import requests
from bs4 import BeautifulSoup
import pandas as pd
from scraping_mesec import funcs

def try_get_title(x):
    try:
        x = str(x)
        split = x.split('"')
        title = split[3]
        return True,title  # Success flag
    except Exception:
        return False,False  # Error flag

def polished(titles):
    cleaned_titles = []
    for x in titles:
        if isinstance(x, bool):
            continue
        if "https" in x or "noopener" in x or x == "":
            continue
        cleaned_titles.append(x)
    return cleaned_titles


url = "https://www.penize.cz/"
result = requests.get(url)
soup = BeautifulSoup(result.text,"html.parser")
found = soup.find_all("div",class_="art")
links = [x.find("a") for x in found]
href = []
titles = []
for link in links:
    if link is not None:
        nlink = link.get("href")
        last = nlink.split("/")[-1]
        first = last.split("-")[0]
        try:
            nirst = int(first)
            if len(nlink) > 40:
                href.append(nlink)
        except:
            pass

    if not try_get_title(link)[0] and type(link) != type(None):   
        title = link.get("h2")
        titles.append(title)
    else:
        titles.append(try_get_title(link)[1])


final_titles = polished(titles)
final = [(title,link) for title,link in zip(final_titles,href)]
instance = funcs()
#print(instance.display_article(articles=final,num=3))
print(final)
