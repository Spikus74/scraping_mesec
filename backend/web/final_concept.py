import requests
from bs4 import BeautifulSoup
import scraping_mesec
import unidecode

def mesec():
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
    return final



def podnikatel():
    URL = "https://www.podnikatel.cz"
    result = requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser")

    found = soup.find_all("a", class_="design-article__heading design-article__link--major design-article__link--default design-article__link")
    final = list()
    links = [x.get("href") for x in found]
    found2 = soup.find_all("h3",class_="element-heading-reset")
    titles = [x.text[1:-1] for x in found2]
    for x in links:
        newlink = URL+x
        index = links.index(x)
        links[index] = newlink
    for title,link in zip(titles,links):
        clean_string = title.replace('\xa0', ' ')
        final.append((clean_string,link))
    return final

def uctovani():
    url = "https://www.uctovani.net/clanky.php"
    received = requests.get(url)
    soup = BeautifulSoup(received.text,"html.parser")

    found = soup.find_all("h3",class_="title")
    elem = [x.find("a") for x in found]
    links = [link.get("href") for link in elem]
    titles = [x.get_text() for x in elem]
    final = {(title,link) for title,link in zip(titles,links)}
    return final

def businessinfo():
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
    return final


podn_final = podnikatel()
mesec_final = mesec()
ucto_final = uctovani()
businessinfo_final = businessinfo()

print(scraping_mesec.funcs.display_article(articles=mesec_final,num=4))