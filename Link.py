# import libraries
import requests
from bs4 import BeautifulSoup

# import Words class (local file)
from Words import Words


class Link:
    def __init__(self, link):
        """
        :param link: str (WebSite link)

        assigning passed link parameter to a link variable
        and initializing a list for linkList and creating a Words object,
        while creating Link object
        """
        self._link = link
        self._links = []
        self._keyWords = Words()
        try:  # use try except for handle possible errors
            """
            getting requests response and pass it to beautifulsoup
            then calling _setLinks
            and at the end we pass beautifulsoup parse data to Words object that we already created
            """
            requestsResponse = requests.get(self._link, timeout=10)
            self.data = BeautifulSoup(requestsResponse.text, "html.parser")
            self._setLinks()
            self._keyWords.setByRequestData(self.data)
        except Exception as e:  # ignore errors
            pass

    def _setLinks(self):
        """
        :return: set self._links

        parsing all anchor tags and append obtained linkList to the _links list
        """
        for item in self.data.findAll('a'):
            calcAttr = item.get('href')
            if calcAttr:
                self._links.append(calcAttr)

    def getLink(self):
        """
        :return: self._link

        getting link of the _link variable
        """
        return self._link

    def getLinks(self):
        """
        :return self._links: list

        getting _links list
        """
        return self._links

    def getWords(self):
        """
        :return self._keyWords: list

        getting _keyWords which is an object of Words class
        """
        return self._keyWords

    def getKeyWords(self):
        """
        :return self._keyWords.getKeyWords(): list (self._keyWords => Words class)

        getting keyWords list from _keyWords object
        """
        return self._keyWords.getKeyWords()
