#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import sqlite3
import re

def get_url(path):
    return "http://jp.finalfantasyxiv.com" + path


def get_soup(url):
    opener = urllib2.build_opener()
    html = opener.open(url).read()
    return BeautifulSoup(html, "html.parser")


class RecipeListParser:
    def __init__(self):
        self.load(1)
        self.last_page = self.get_last_page_number()

    def load(self, page_number):
        self.soup = get_soup(self.get_page_url(page_number))
        
    def get_page_url(self, page_number):
        return get_url("/lodestone/playguide/db/recipe/?page=%s" % page_number)

    def get_last_page_number(self):
        pager = self.soup.find("div", {"class" : "pager"})
        next_all = pager.find("li", {"class" : "next_all"})
        url = next_all.find("a")["href"]

        return int(re.search(r"page=(\d+)", url).group(1))

    def get_recipe_id_list(self, page_number):
        self.load(page_number)
        recipe_list = self.soup.find_all("a", {"class" : "db-table__txt--detail_link"})
        recipe_id_list = []
        for i in recipe_list:
            recipe_id = re.search(r"\/recipe\/(\w+)\/", i["href"]).group(1) 
            recipe_id_list.append(recipe_id)
        return recipe_id_list

class RecipeParser:
    def __init__(self, recipe_id):
        self.load(recipe_id)

    def load(self, recipe_id):
        self.soup = get_soup(self.get_recipe_url(recipe_id))
        
    def get_recipe_url(self, recipe_id):
        return get_url("/lodestone/playguide/db/recipe/%s/" % recipe_id)

    def get_item_id(self):
        item = self.soup.find("div", {"class" : "db-tooltip__bt_item_detail"}).find("a")
        return re.search(r"\/item\/(\w+)\/", item["href"]).group(1) 

    
# クラフタ職業
# 作成レベル
# 完成品ID x 個数
# 素材ID x 個数
# クリスタル x 個数
# 必要工数
# 耐久
# 品質最大値
    
def main():
    list_parser = RecipeListParser()

    for num in range(1, list_parser.get_last_page_number() + 1):
        print "Page = %s" % num
        recipe_id_list = list_parser.get_recipe_id_list(num)
        for recipe_id in recipe_id_list:
            recipe_parser = RecipeParser(recipe_id)
            print recipe_parser.get_item_id()

if __name__ == "__main__":
    main()
