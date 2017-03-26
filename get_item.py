#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import sqlite3
import re

class ItemPageParser:
    def __init__(self):
        self.page = 1

    def get_url(self, path):
        return "http://jp.finalfantasyxiv.com" + path

    def get_page_url(self, page):
        return self.get_url("/lodestone/playguide/db/item/?page=%s" % str(page))

    def get_last_page_number(self, html):
        soup = BeautifulSoup(html, "html.parser")
        pager = soup("div", {"class" : "pager"})[0]
        next_all = pager("li", {"class" : "next_all"})[0]

        url = next_all.find("a")["href"]

        return re.search(r"page=(\d+)", url).group(1)

    def get_item_list(self, html):
        soup = BeautifulSoup(html, "html.parser")

        div_item = soup("div", {"class" : "db-list__item__icon__cover db_popup"})
        item_url_list = []
        for i in div_item:
            item_url_list.append(self.get_url(i.get("data-ldst-href")))

        return item_url_list


def parseItemPage(html):
    soup = BeautifulSoup(html)
    item_detail = soup('div', {'class' : 'item_detail_box'})[0]
    name = item_detail('h2')[0].get_text()

    print name

def main():
    item_parser = ItemPageParser()

    opener = urllib2.build_opener()
    
    html = opener.open(item_parser.get_page_url(1)).read()
    last_page = item_parser.get_last_page_number(html)
    print 'last page = %s' % last_page

    i = 1
    
    while True:
        print 'parsing page ' + str(i)
        html = opener.open(item_parser.get_page_url(i)).read()
        item_url_list = item_parser.get_item_list(html)

        print item_url_list

        i += 1
        if i > last_page:
            break
        

if __name__ == "__main__":
    main()
