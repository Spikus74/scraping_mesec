import requests
from bs4 import BeautifulSoup
from scraping_mesec import funcs
import unidecode

# backend.web.final_concept
def mesec():
    print ("scraping mesec.cz")
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
    print ("scraping podnikatel.cz")
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
    h3_tags = soup.find_all('h3', class_='title')
    concatter = "https://www.uctovani.net/"
    links = [concatter+link.find('a')["href"] for link in h3_tags]
    titles = [title.find("a").get_text() for title in h3_tags]
    final = [(title,link) for title,link in zip(titles,links)]
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
        title[title.index(x)] = x
    pretitles = [t for t in title]
    final_titles = [x.encode("latin1").decode("utf-8") for x in pretitles]
    final = [(title,link) for title,link in zip(final_titles,final_links)]
    return final

def mpo():
    url = "https://www.mpo.cz/"
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")

    elem = soup.find('div', class_='block_news_top').find_all("a")
    links = [link.get("href") for link in elem]
    links = links[1:-1][::3]
    all_links = [url+x for x in links]

    h3_element = soup.find_all("h3")
    final_titles = []
    for elem in h3_element:
        if elem:
            text = elem.text
            final_titles.append(text.encode("latin1").decode("utf-8"))

    final = [(title,link) for title,link in zip(final_titles,all_links)]
    return final

if __name__ == "__main__":
    instance = funcs()
    print(instance.display_article(articles=mpo(),num=1))


