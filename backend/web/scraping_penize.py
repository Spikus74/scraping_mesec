import requests
from bs4 import BeautifulSoup
import pandas as pd

def try_get_title(x):
    try:
        x = str(x)
        split = x.split('"')
        title = split[3]
        return True,title  # Success flag
    except Exception as e:
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
for link in links:
    if link is not None:
        nlink = link.get("href")
        href.append(nlink)

for x in href:
    last = x.split("/")[-1]
    first = last.split("-")[0]
    try:
        first = int(first)
    except:
        href.pop(href.index(x))

titles = []
for x in links:
    if not try_get_title(x)[0] and type(x) != type(None):   
        title = x.get("h2")
        titles.append(title)
    else:
        titles.append(try_get_title(x)[1])

for x in href:
    if len(x) < 40:
        href.pop(href.index(x))

final_titles = polished(titles)
final = {title:link for title,link in zip(final_titles,href)}
last_values = [value.split("/")[-1] for value in final.values()]   #just for testing
print(pd.DataFrame(last_values,index=final.keys()))    #remove the dataframe for final version
