import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

class Figure:
    def __init__(self,image,caption) -> None:
        self.image = image
        self.caption = caption
        pass

class Content:
    def __init__(self,tags) -> None:
        self.tags = tags
        pass

    def get_only_text(self) -> str:
        text_tags = self.tags.findAll("p")
        text_tags_texts = [tag.text for tag in text_tags]
        return "".join(text_tags_texts)
    
    def get_only_figures(self) -> list[Figure]:
        figures = []
        figure_tags = self.tags.findAll("figure")
        for figure in figure_tags:
            fig = figure.find("img")
            caption = fig["alt"]
            image = fig["src"]
            figures.append(Figure(image,caption))


class Article:
    """
    A class to modelize El Pais newspaper articles
    """
    def __init__(self) -> None:
        pass

    def _set_title(self,title : str) -> None:
        self.title = title

    def _set_link(self,link : str) -> None:
        self.link = link

    def _set_image(self,image : str) -> None:
        self.image = image

    def _set_content(self,free : bool):
        self.has_content = free
        if free:
            response = requests.get(self.link)
            soup = BeautifulSoup(response.text,"html.parser")
            tags = soup.find("div",{"data-dtm-region" : "articulo_cuerpo"})
            self.content = Content(tags)
        else:
            self.content = None

class ElPais:
    """
    A class to modelize El Pais newspapers
    """
    def __init__(self) -> None:
        pass

    def get_articles(self) -> list[Article]:
        articles = []
        response = requests.get("https://elpais.com/")
        soup = BeautifulSoup(response.text,"html.parser")
        n = 0
        for div in soup.findAll("article"):
            article = Article()
            try:
                image = div.find('img')['src']
            except:
                image = None
            article._set_image(image)
            title = div.find('header').text
            article._set_title(title)
            link = div.find('a')['href']
            article._set_link(link)

            # check if article is free
            if div.find("span",{'name' : "elpais_ico"}) == None:
                article._set_content(True)
            else:
                article._set_content(False)
            articles.append(article)
            n+= 1
            if n>100:
                break
        
        return articles








