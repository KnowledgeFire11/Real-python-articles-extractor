import requests
from bs4 import BeautifulSoup
import time
import concurrent.futures

# Start of program
print("Welcome the program!")
print("Please enter the name of the topic you would want to browse through: ")
print("If you want the topics enter 'List'")
while True:
    topic_name = input(">> ").lower().strip()
    topics = ['advanced', 'api', 'basics', 'best-practices', "community", 'databases', "data-science", 'devops', 'django',
              'docker', 'flask', 'front-end', 'intermediate', 'machine-learning', 'python', 'testing', 'tools', 'web-dev', 'web-scraping']
    if topic_name == 'list':
        for index, topic in enumerate(topics):
            print(f"{index+1}) {topic.capitalize()}")
    elif topic_name in topics:
        print(
            f"Here are the articles of {topic_name.capitalize()}.(This may take a few seconds to minutes based on your internet connection)")
        break
    else:
        print("We are sorry but that topic is not on the website")

start = time.perf_counter()
source = requests.get(
    f"https://realpython.com/tutorials/{topic_name}/page/1/").text
soup = BeautifulSoup(source, 'lxml')
if soup.find('nav', attrs={'aria-label': 'Page Navigation'}):
    no_of_pages_in_topic = soup.find(
        'nav', attrs={'aria-label': 'Page Navigation'})
    no_of_pages = []
    for x in no_of_pages_in_topic.ul.children:
        if x != '\n':
            no_of_pages.append(x)

    no_of_pages = len(no_of_pages)-2
else:
    no_of_pages = 1


def get_articles(page_no):

    source = requests.get(
        f"https://realpython.com/tutorials/{topic_name}/page/{page_no}/").text
    soup = BeautifulSoup(source, 'lxml')
    for article in soup.find_all('div', class_='card border-0'):
        heading = article.h2.text
        link = article.a.attrs['href']
        if article.find('i', class_='fa fa-star text-muted'):
            premium = True
        else:
            premium = False

        print(
            f"\nHeading: {heading}\nLink : https://realpython.com{link}\nPremium : {premium}")
        # print(f"Link : https://realpython.com{link}")
        # print(f"Premium : {premium}")


with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(get_articles, x)
               for x in range(1, no_of_pages+1)]
    #executor.map(get_articles, [x for x in range(1, no_of_pages+1)])


finish = time.perf_counter()


print(f"The program took {round(finish-start,2)} seconds to complete")
