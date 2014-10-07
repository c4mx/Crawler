__author__ = 'Jianqiao'

from bs4 import BeautifulSoup
import re
import requests


class Crawler:
    def __init__(self, root_link):
        self.current_depth = 1
        self.link_queue = LinkQueue()
        if isinstance(root_link, str):
            self.link_queue.add_unvisited_link_list(root_link)
        elif isinstance(root_link, list):
            for link in root_link:
                self.link_queue.add_unvisited_link_list(link)
        print("Add the root link {links}".format(links=self.link_queue.unvisited_link_list))

    def process_craw(self, crawl_depth):
        while self.current_depth <= crawl_depth:
            while not self.link_queue.unvisited_link_list_empty():
                to_visit_link = self.link_queue.unvisited_link_list_dequeue()
                print("Pop out one link {link}".format(link=to_visit_link))
                if to_visit_link is None or to_visit_link == "":
                    continue
                links = get_links_from_link(to_visit_link)
                print("Get {num} news links".format(num=len(links)))
                for link in links:
                    self.link_queue.add_unvisited_link_list(link)
                self.link_queue.add_visited_link_list(to_visit_link)
                print("Visited link number: {num}".format(num=self.link_queue.get_visited_links_num()))
                print("Crawl depth: {depth}".format(depth=self.current_depth))
            print("{num} unvisited links:".format(num=self.link_queue.get_unvisited_links()))
            self.current_depth += 1


class LinkQueue:
    def __init__(self):
        # A list of all visited links
        self.visited_link_list = []
        # A list of all links waiting for visit
        self.unvisited_link_list = []

    def get_visited_links(self):
        """Get the visited links list"""
        return self.visited_link_list

    def get_unvisited_links(self):
        """Get the unvisited links list"""
        return self.unvisited_link_list

    def add_visited_link_list(self, link):
        """Add a visited link to visited links list"""
        self.visited_link_list.append(link)

    def unvisited_link_list_dequeue(self):
        """Remove and return the last link in the visited links list"""
        try:
            return self.unvisited_link_list.pop()
        except:
            return None

    def add_unvisited_link_list(self, link):
        """Add a unvisited link to the unvisited link list"""
        if link != "" and link not in self.unvisited_link_list and link not in self.visited_link_list:
            self.unvisited_link_list.insert(0, link)

    def get_visited_links_num(self):
        """Get the number of the visited links"""
        return len(self.visited_link_list)

    def get_unvisited_links_num(self):
        """Get the number of the unvisited links"""
        return len(self.unvisited_link_list)

    def unvisited_link_list_empty(self):
        """if unvisited links list is empty, return True"""
        return len(self.unvisited_link_list) == 0


# Scoop all the links in a html page and return them by a links list
def get_links_from_link(link):
    links = []
    try:
        r = requests.get(link)
        r.encoding = 'gb2312'
        soup = BeautifulSoup(r.text)
    except:
        pass
    else:
        for tag_a in soup.find_all('a', href=True):
            links.append(tag_a.get('href'))
    return links


# Search a key-word in a beautiful soup object
# If find a key-word, return True
def search_key_word(soup, key_word):
    text = soup.get_text()
    result = re.findall(re.escape(key_word), text)
    if result:
        return True
    else:
        return False


def main(root_link, crawl_depth):
    craw = Crawler(root_link)
    craw.process_craw(crawl_depth)

if __name__ == "__main__":
    main(["http://www.sina.com.cn"], 3)



