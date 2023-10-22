import requests
from bs4 import BeautifulSoup
import numpy as np
import re

URL = "https://www.mesec.cz"
result = requests.get(URL)
soup = BeautifulSoup(result.text, "html.parser")


element_with_class = soup.find("ul", class_="design-list--articles--tiles--rows--small design-list--articles--tiles--rows design-list--articles--tiles design-list--articles design-list list-reset")

elem = element_with_class.find_all("a")
links = [link.get("href") for link in elem]
titles = []

for link in links:
    pretitle = link.split("/")[-2]
    title_list = pretitle.split("-")
    title = ""
    for x in title_list:
        title += x + " "
    titles.append(title)

final = []
for link in links:
    newlink = "https://www.mesec.cz" + link
    ind = links.index(link)
    links.pop(ind)
    links.insert(ind,newlink)
for title,link in zip(titles,links):
    final.append((title,link))

class funcs:
    def clean(self,article):
        article = str(article)
        cleaned_article = []
        inside_tag = False

        for char in article:
            if char == "<":
                inside_tag = True
            elif char == ">":
                inside_tag = False
            elif not inside_tag:
                cleaned_article.append(char)

        cleaned_text = "".join(cleaned_article)
        cleaned_text = cleaned_text.replace(" , , "," ")
        cleaned_text = cleaned_text.replace("., ",". ")
        cleaned_text = cleaned_text.replace(" , "," ")
        cleaned_text = cleaned_text.replace(":, ",": ")
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

        return cleaned_text



    def display_article(self,articles,num):
        unit = articles[num]
        result = requests.get(unit[1])
        soup = BeautifulSoup(result.text,"html.parser")
        text = soup.find_all("p")
        text = self.clean(text)
        return text
    
myfunc = funcs()
for x in final:
    if final.count(x) > 1:
        final.remove(x)

print(myfunc.display_article(articles=final,num=0))