# import libraries
import threading
import time
from urllib.parse import urlparse
from Link import Link

# import Words class and bubble sort (local file)
from Words import Words
from BubbleSort import BubbleSort

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

    while len(links) and (time.time() - startTime) < 295:
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
for _ in range(4):  # create other threads
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
