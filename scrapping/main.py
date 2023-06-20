import os
import urllib
import requests
from bs4 import BeautifulSoup
from db_data import insert
import urllib
import re
import yaml
import sys
# from selenium import webdriver
import sqlite3
user_agent = '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'

headers = {'User-Agent' : user_agent }


links_data__ = "https://www.pdfdrive.com/animation-books.html"

data_1 = list()
data_dict = dict()


class scraping(object):
    def __init__(self):
        super(scraping, self).__init__()
        self.create_paginations_links()

    def scraping_link(self):
        links__ = list()
        if data_1 == []:
            return

        for links_data in data_1:

            response = requests.get(links_data)
            soup = BeautifulSoup(response.content, 'html.parser')
            get_link = soup.findAll('div', 'file-right')

            for links in get_link:
                pages_links = "{}".format(links)

                soup__ = BeautifulSoup(pages_links, 'html.parser')
                find_link = soup__.findAll('a')
                for page_links in find_link:
                    format_string = "{}".format(page_links).partition('href="/')[2].partition('"')[0]
                    make_link = "https://www.pdfdrive.com/{}".format(format_string)

                    links__.append(make_link)
                    get_text = "{}".format(soup)

        # description = get_text.partition("</div>")[2].partition("</div>")[0]
        # self.final_description = description.replace("</b>", "").replace("<b>", "")
        # print self.final_description
        remove_duplicate = list(set(links__))

        for data in remove_duplicate:
            print">>>", data
            response = requests.get(data)
            soup_ = BeautifulSoup(response.content, 'html.parser')
            find_title = soup_.findAll('h1', 'ebook-title')

            find_info = soup_.find('img', 'ebook-img')
            image = find_info['src']
            data_dict['image'] = image
            find_author = soup_.findAll('div', 'ebook-author')
            for author in find_author:
                authors = '{}'.format(author).partition('"creator">')[2].partition('</span>')[0]
                data_dict['authors'] = authors

            for data in find_title:
                title = data.text
                data_dict['title'] = title

            find_info = soup_.findAll("span", "info-green")
            pages = find_info[0]
            pages_ = '{}'.format(pages).partition('"info-green">')[2].partition('</span>')[0]
            data_dict['pages'] = pages_
            year = find_info[1]
            year_ = '{}'.format(year).partition('"info-green">')[2].partition('</span>')[0]
            data_dict['year'] = year_
            size = find_info[2]
            size_ = '{}'.format(size).partition('"info-green">')[2].partition('</span>')[0]
            data_dict['size_'] = size_
            language = find_info[4]
            language_ = '{}'.format(language).partition('"info-green">')[2].partition('</span>')[0]
            data_dict['language'] = language_

            download_link = soup_.find('div', 'dropdown-menu dropdown-menu-right')
            download = '{}'.format(download_link).partition('"initConverter(')[2].partition(",'EPUB'")[0]
            get_list = download.split(",")
            value_1 = get_list[0]
            value = value_1.replace("'", "")
            value_2 = get_list[1]
            value_ = value_2.replace("'", "")
            final_downlaod_link = "https://www.pdfdrive.com/download.pdf?id={}&h={}&u=cache&ext=pdf".format(value,
                                                                                                            value_)
            data_dict['download_url'] = final_downlaod_link

            title = data_dict.get('title')
            image = data_dict.get('image')
            pages = data_dict.get('pages')
            size = data_dict.get('size_')
            year = data_dict.get('year')
            language = data_dict.get('language')
            downlaod = data_dict.get('download_url')
            author = data_dict.get('authors')
            print downlaod, image, pages

            insert(title=title, image=image, pages=pages, size=size, year=year, language=language,
                   download_url=downlaod, categories="Biology", authors=author)

    def create_paginations_links(self):
        main_links = list()
        numbers = []
        max_ = dict()
        response = requests.get(links_data__, headers=headers)
        print ">>>>>>> dsata"
        soup = BeautifulSoup(response.content, 'html.parser')
        print soup
        get_pagination = soup.findAll('div', 'pagination')
        print get_pagination
        for paginations in get_pagination:
            page_pages = "{}".format(paginations)
            soup___ = BeautifulSoup(page_pages, 'html.parser')
            find_links_ = soup___.findAll('a')

            for data in find_links_:
                pagination_links_ = "{}".format(data)
                make = BeautifulSoup(pagination_links_, 'html.parser')
                find_l = make.findAll('a')
                for data_ in find_l:
                    make_link__ = "{}".format(data_)
                    make_page_links = make_link__.partition('href="')[2].partition('"')[0]

                    make = make_page_links.replace(" ", "%20")
                    make_real_link = make.replace("amp;", "")

                    main_links.append(make_real_link)
                    pagi_links = pagination_links_.partition('nofollow">')[2].partition('</a>')[0]

                    numbers.append(pagi_links)
                    max_['data'] = numbers

            links_2 = list()
            links_ = list()
            get_numbers = max_.get('data')
            get_numbers.pop(0)
            get_numbers.pop(-1)
            map_list = [int(data) for data in get_numbers]
            maximum_number = max(map_list)
            print maximum_number
            for pagination in main_links:
                make_link = pagination.partition('&page=')[0]
                links_.append(make_link)
            for i in range(1, maximum_number + 1):
                for data in links_:
                    _link = "http://www.pdfdrive.com/{}&page={}".format(data, i)
                    links_2.append(_link)

            remove_duplicate = list(set(links_2))

            for data in remove_duplicate:
                data_1.append(data)

        self.scraping_link()


if __name__ == "__main__":
    scraping()
