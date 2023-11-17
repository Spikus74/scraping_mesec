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
        if "nazory" in link:
            nlink = link.split("nazory")[0]
            ind = links.index(link)
            links.pop(ind)
            links.insert(ind,nlink)

    for link in links:
        pretitles = link.split("/")
        pretitle = max(pretitles,key=len)
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
    final = list(set(final))
    final = [(name, link) for name, link in final if "autori" not in link]
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

    titles = [max(link.split("/"),key=len).replace("-"," ") for link in final_links]
    final = [(title,link) for title,link in zip(titles,final_links)]
    return final  #články a nadpisy se negroupují správně; text se neuhladí (doesnt get polished) správně

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

def kurzy():
    url = "https://www.kurzy.cz/zpravy/"
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")

    elem = soup.find("div",class_="hlavnizpravy ecb").find_all("a")
    links = [link.get("href") for link in elem]
    titles = [title.text for title in elem]
    links = links[1:][::2]
    titles = titles[1:][::2]
    final = [(title,link) for title,link in zip(titles,links)]
    return final #funkce display tuto stránku nezobrazuje správně

def display(funcs,articles,num):
    unit = articles[num]
    result = requests.get(unit[1])
    for encoding in ['utf-8', 'iso-8859-1', 'windows-1250', 'cp1250', 'cp1252']:
            try:
                # Parse the HTML content using the selected encoding
                soup = BeautifulSoup(result.content, 'html.parser', from_encoding=encoding)
                text = soup.find_all(["p","h2"])
                formatted_text = ":".join(str(element) for element in text)
                cleaned_text = funcs.clean(formatted_text)
                #return cleaned_text
            except Exception as e:
                continue
    return cleaned_text

class final_cleaning():
    def __init__(self,text):
        self.text = text

    def businessinfo(self):
        result = self.text.split("BusinessInfo.cz")
        length = 0
        output = ""
        for x in result:
            if len(x) > 100:
                output += x
        return output
        
    
    def mesec_a_podnikatel(self):
        return self.text.lstrip("[ Zapomenuté heslo nebo jméno , Sdílet")
    
    def uctovani(self):
        return self.text.lstrip("[ Chcete podnikat v oblasti účetnictví? Zveme vás do naší nové Facebookové skupiny, která je určena pro všechny, kteří se touží osamostatnit a stát se tak svobodnou účetní. , ")

    def mpo(self):
        return self.text.lstrip("[ Přeskočit na: navigaci | hlavní obsah stránky , ")
    
    def kurzy(self):
        text = self.text.split("Další vybrané zprávy »:")
        return text[1]
    

if __name__ == "__main__":
    instance = funcs()
    func = kurzy()
    num = 1
    title = func[num][0]
    text = display(instance,func,num=num)
    clean = final_cleaning(text)
    if func == businessinfo():
        text = clean.businessinfo()
    elif func == mesec() or func == podnikatel():
        text = clean.mesec_a_podnikatel()
    elif func == uctovani():
        text = clean.uctovani()
    elif func == mpo():
        text = clean.mpo()
    elif func == kurzy():
        text = clean.kurzy()

    print(title)
    print("\n")
    print(text)
    print("\n")
    print(func)





