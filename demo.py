# import libraries
import threading
import time
from urllib.parse import urlparse
from statistics import mean, StatisticsError
import requests
from bs4 import BeautifulSoup


def BubbleSort(array):
    # custom bubble sort for priority queue
    """
    :param array: list([], [])
    :return: sorted list
    """
    for i in range(len(array[0])):
        for j in range(i + 1, len(array[0])):
            if array[0][i] < array[0][j]:
                array[0][i], array[0][j] = array[0][j], array[0][i]  # for priority
                array[1][i], array[1][j] = array[1][j], array[1][i]  # for value


# creating a list of english stop words
stopWords = ['a', 'ourselves', 'about', 'out', 'above', 'over', 'after', 'own', 'again', 'same', 'against', "shan't",
             'all', 'she', 'am', "she'd", 'an', "she'll", 'and', "she's", 'any', 'should', 'are', "shouldn't", "aren't",
             'so', 'as', 'some', 'at', 'such', 'be', 'than', 'because', 'that', 'been', "that's", 'before', 'the',
             'being', 'their', 'below', 'theirs', 'between', 'them', 'both', 'themselves', 'but', 'then', 'by', 'there',
             "can't", "there's", 'cannot', 'these', 'could', 'they', "couldn't", "they'd", 'did', "they'll", "didn't",
             "they're", 'do', "they've", 'does', 'this', "doesn't", 'those', 'doing', 'through', "don't", 'to', 'down',
             'too', 'during', 'under', 'each', 'until', 'few', 'up', 'for', 'very', 'from', 'was', 'further', "wasn't",
             'had', 'we', "hadn't", "we'd", 'has', "we'll", "hasn't", "we're", 'have', "we've", "haven't", 'were',
             'having', "weren't", 'he', 'what', "he'd", "what's", "he'll", 'when', "he's", "when's", 'her', 'where',
             'here', "where's", "here's", 'which', 'hers', 'while', 'herself', 'who', 'him', "who's", 'himself', 'whom',
             'his', 'why', 'how', "why's", "how's", 'with', 'i', "won't", "i'd", 'would', "i'll", "wouldn't", "i'm",
             'you', "i've", "you'd", 'if', "you'll", 'in', "you're", 'into', "you've", 'is', 'your', "isn't", 'yours',
             'it', 'yourself', "it's", 'yourselves', 'its', 'nor', 'itself', 'not', "let's", 'of', 'me', 'off', 'more',
             'on', 'most', 'once', "mustn't", 'only', 'my', 'or', 'myself', 'other', 'no', 'ought', 'ours', 'our',
             'also']


class Words:
    """
    creating Words class which its objects will use beautifulsoup data to determine keywords
    """

    def __init__(self):
        """
        creating words and keywords lists
        """
        self._words = []
        self._keyWords = []

    def setByRequestData(self, data):
        """
        :param data: requests result
        :return: call self._setWords & self._calcKeyWords()

        set _words and _keywords value by beautifulsoup parsed data
        """
        self._setWords(data)
        self._calcKeyWords()

    def setByString(self, data):
        """
        :param data: str
        :return: call self._dumpRemove & self._calcKeyWords()

        set _words and _keywords value by string data
        """
        self._dumpRemove(data, 1)
        self._synonymsWord()
        self._calcKeyWords()

    def similarityRate(self, other):
        """
        :param other: Words Class
        :return output: int (similarity rate)

        receiving in other words object as parameter and return their keywords similarity
        """
        # similarity rate
        output = 0

        # looping through words and values in keywords list of both objects and check their similarity
        for wordOut, valueOut in other.getKeyWords():  # for other class
            for wordIn, valueIn in self._keyWords:  # foe this class
                if wordIn == wordOut:
                    output += valueIn * valueOut

        return output

    def _synonymsWord(self):
        """
        :return: add any Dword synonyms

        getting synonyms of words in _words list and then add them all to _words list again
        """

        # creating a helper list (used like stack or queue)
        wordsList = [i for i in self._words]

        while len(wordsList) != 0:
            calc = wordsList.pop()
            try:  # use try except for handle possible errors
                pass
                # using words.bighugelabs.com API to get synonyms
                synonyms = requests.get("https://words.bighugelabs.com/api/2/419ddff26f1a04fd2b9629291c5a1350/"
                                        + calc + "/json", timeout=20).json()["noun"]["syn"]
                synonyms = list(filter(lambda item: item.find(" ") == -1, synonyms))
                self._words += synonyms
            except Exception as e:  # ignore errors
                pass

    def _dumpRemove(self, text, rep):
        """
        :param text: str
        :param rep: int
        :return: update self._words

        check if words in formatted text are in stopwords or not, then add them to words list by their repetition
        """

        # check words len
        if len(self._words) > 2000:  # check words count
            return

            # formatting and splitting text
        calcWords = text.lower().replace("?", "").replace("-", "").replace("\"", "").replace("(", "").replace(")", "") \
            .replace("^", "").replace("•", "").replace(".", "").replace(",", "").replace("*", "").replace("&", "") \
            .replace("/", "").replace("+", "").replace("_", "").replace("|", "").replace("#", "").replace("\\", "") \
            .split()

        # omitting stop words
        calcWords = list(filter(lambda Dword: Dword not in stopWords, calcWords))

        # adding words to _words list according to the number of their repetitions
        for i in range(rep):
            if len(self._words) >= 2000:  # check words count
                break
            for word in calcWords:
                if len(self._words) >= 2000:  # check words count
                    break
                self._words.append(word)

    def _setWords(self, data):
        """
        :param data: requests result
        :return: call self._dumpRemove

        searching for different HTML tags and calling self._dumpRemove on them
        depending on tags importance, they get a different rep value which will help us to determine keywords
        """

        try:  # use try except for handle possible errors

            # parsing meta (name = keyword) tag
            # meta tag content is the most valuable because have keywords of web page
            for item in data.findAll('meta'):
                if item.get("name") == "keyword":
                    self._dumpRemove(item.get("content"), 20)

            # parsing img alt
            for item in data.findAll("img"):
                self._dumpRemove(item.get("alt"), 6)

            # parsing h1 tag
            for item in data.findAll('h1'):
                self._dumpRemove(item.text, 6)

            # parsing h2 tag
            for item in data.findAll('h2'):
                self._dumpRemove(item.text, 5)

            # parsing h3 tag
            for item in data.findAll('h3'):
                self._dumpRemove(item.text, 4)

            # parsing h4 tag
            for item in data.findAll('h4'):
                self._dumpRemove(item.text, 3)

            # parsing h5 tag
            for item in data.findAll('h5'):
                self._dumpRemove(item.text, 2)

            # parsing h6 tag
            for item in data.findAll('h6'):
                self._dumpRemove(item.text, 1)

            # parsing p tag
            for item in data.findAll('p'):
                self._dumpRemove(item.text, 1)

            # parsing b tag
            for item in data.findAll('b'):
                self._dumpRemove(item.text, 1)

            # parsing strong tag
            for item in data.findAll('strong'):
                self._dumpRemove(item.text, 1)
        except Exception as e:  # ignore errors
            pass

    def _calcKeyWords(self):
        """
        :return: set self._keyWords

        counting words and made 2D list => list[0][index] = count(Dword), list[0][index] = Dword
         and finally set _keyWords value
        """
        # removing repetitive words by creating a set of them
        uniqueWord = set(self._words)

        # creating a 2D array that will store words and the number of repetition of those words
        countWord = [[], []]

        for i in uniqueWord:
            countWord[0].append(self._words.count(i))
            countWord[1].append(i)

        # sorting the 2D list
        BubbleSort(countWord)
        # check if keywords are more than 15
        if len(countWord[0]) > 30:
            # if number of a Dword is more than the mean of other words, we will add it to keywords list
            try:
                checkindex = 0
                while countWord[0][checkindex] >= mean(countWord[0][0:(len(countWord[0]) // 15)]):
                    # if number of a Dword is more than the mean of other words, we will add it to keywords list
                    self._keyWords.append((countWord[1][checkindex], countWord[0][checkindex]))
                    checkindex += 1
                # if keywords in 2D list are less than or equal to 15, we will add them all
            except StatisticsError as e:
                print("words not found")
        else:
            self._keyWords = [(countWord[1][i], countWord[0][i]) for i in range(min(len(countWord[0]), 15))]

    def getKeyWords(self):
        """
        :return: self._keyWords

        getting keywords list
        """
        return self._keyWords


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


startLink = input("Enter start link: ")  # for example https://en.wikipedia.org/wiki/Man

# linkList list (used like stack and queue)
links = [startLink]

# creating some empty lists to use in the following while loop
checkedLinks = []  # save checked linkList
checkedDomains = []  # save checked domain
linkClasses = []  # save link classes foe search

# save start time foe end of loop
startTime = time.time()

# log file
logFile = open("logs/log_" + str(startTime) + ".txt", "w")

# write log
logFile.write("Start Crawling\n")


# main loop
# resuming while loop until its execution time doesn't exceed our time limit
def linkOperating():
    global links, checkedLinks, checkedDomains  # use global variables

    while len(links) and (time.time() - startTime) < 300:
        calcLink = links.pop()

        # parse URL
        try:
            domain = urlparse(calcLink).netloc

            # if domain we got does not exist in checkedDomains list:
            if domain and domain not in checkedDomains:
                checkedLinks.append(calcLink)
                checkedDomains.append(domain)

                # creating a Link object named webPage, and pass a link as its parameter
                webPage = Link(calcLink)

                # add web page links to links list
                links += webPage.getLinks()

                # write logs
                try:
                    logFile.write(calcLink + " : " + str(webPage.getKeyWords()) + "\n")
                except Exception as e:
                    pass

                # appending Link objects to linkClasses list
                linkClasses.append(webPage)
        except Exception as e:
            pass


# Handle multithreading

# run First thread sooner because len(checkedLinks) > 100
firstThread = threading.Thread(target=linkOperating)
firstThread.start()
time.sleep(5)  # use sleep => len(checkedLinks) > 100
threads = []  # save threads
for _ in range(29):  # create other threads
    t = threading.Thread(target=linkOperating)
    t.start()
    threads.append(t)

# join all threads
firstThread.join()
for thread in threads:
    thread.join()

# write logs
logFile.write("Done Crawling\n")
logFile.write((str(len(linkClasses)) + " webpages scanned\n\n"))
print(str(len(linkClasses)) + " webpages scanned")

# creating a 2D list to store search result
searchResult = [[], []]

# getting a string from the user
searchStr = input("Enter search sentence:")

# creating an object from Words class
searchWords = Words()

# pass input string to searchWords object
searchWords.setByString(searchStr)

# write log
logFile.write("Search: " + searchStr + " => " + str(searchWords.getKeyWords()) + "\n")
# looping through Link objects which are in linkClasses list
for site in linkClasses:
    # comparing two objects from the Words class and calculating their similarity rate
    calcRes = searchWords.similarityRate(site.getWords())
    if calcRes != 0:
        searchResult[0].append(calcRes)
        searchResult[1].append(site.getLink())

# sorting the 2D list
BubbleSort(searchResult)

print("Results for \"" + searchStr + "\":")

# write log
logFile.write("\nSearch Results\n")

# printing searchResult list
for i in searchResult[1]:
    # print linkList
    print(i)

    # write logs
    logFile.write(i + "\n")

# logs
print("4001406134 4001406149")
logFile.write("\n\n4001406134 4001406149")
logFile.close()
