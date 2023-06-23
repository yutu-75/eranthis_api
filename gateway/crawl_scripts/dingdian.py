import datetime
import json
import time
import uuid

import requests
from lxml import etree
from bs4 import BeautifulSoup
from gateway.crawl_scripts.book_data import book_all_list
from gateway.crawl_scripts.to_db_data_const import to_db_data
from internal.common.gen_random_obj import get_new_uuid
from internal.db.mongo.mongo_api import get_mongo_client
from utils.logger import setup_log

logger = setup_log('crawl_scripts')

search_all_list = []


class ReptileClient:
    def __init__(self):
        self.url = "https://www.23dd.cc"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/108.0.0.0 Safari/537.36",
        }
        self.book_list = book_all_list
        self.proxies = {
            'http': '127.0.0.1:7890',
            'https': '127.0.0.1:7890'
        }

    def get_response_text(self, url):
        s_time = datetime.datetime.now()
        response = requests.get(url=url, headers=self.headers)
        response.encoding = "gbk"

        logger.info(f"status_code:{response.status_code}\nTime Used:{datetime.datetime.now() - s_time}")

        if response.status_code != 200:
            logger.error(f"url:{url}\n"+response.text + f"\n{datetime.datetime.now() - s_time}")
            raise Exception("get error!!!")

        return response.text

    def get_book_data_list(self, page):
        time.sleep(1)
        response = self.get_response_text(f"https://www.23dd.cc/quanben/{page}")
        tree = etree.HTML(response)

        n = 1
        sign = True
        while sign:
            book_name = tree.xpath(f'//tr[{n + 1}]/td[1]//text()')
            # print(book_name)
            author = tree.xpath(f'//tr[{n + 1}]/td[3]//text()')
            # print(author)
            book_url = tree.xpath(f'//tr[{n + 1}]/td[1]//@href')
            # print(book_url)

            if not book_name:
                sign = False
                break
            n += 1
            book_data = {
                "book_name": book_name[0],
                "author": author[0],
                "book_url": book_url
            }
            search_all_list.append(book_data)

            print(book_data)

    def search_book(self, book_name):
        """
        搜索书名是否存在,并反回url路径
        """
        search_list = []
        for i in self.book_list:
            if book_name in i["book_name"] or book_name in i["author"]:
                search_list.append(i)
        return search_list

    def get_book_chapter(self, url):
        """
        获取简介,图书封面,章节名,url地址
        """
        response = self.get_response_text(url)
        tree = etree.HTML(response)
        chapter_all_list = []
        n = 1
        sign = True
        while sign:
            text_list = tree.xpath(f"//*[@id='list']/dl/dd[{n}]/a//text()")
            href_list = tree.xpath(f"//*[@id='list']/dl/dd[{n}]/a//@href")
            if not text_list:
                break
            chapter_all_list.append({
                "chapter_name": text_list[0],
                "chapter_url": to_db_data["book_url"] + href_list[0]
            })
            n += 1
        book_img = tree.xpath(f"//*[@id='fmimg']/img//@src")
        book_blurb = tree.xpath(f"//*[@id='intro']/p//text()")

        result = {
            "book_data": {
                "book_img": self.url + book_img[0] if book_img else "",
                "book_blurb": book_blurb[0].replace("\xa0", " ") if book_blurb else ""
            },
            "chapter_all_list": chapter_all_list
        }
        return result

    def get_book_content(self, url):
        """
        获取章节内容
        """
        response = self.get_response_text(url)
        soup = BeautifulSoup(response, "lxml")
        tag = soup.select_one("#content")
        book_content = tag.text.replace(url.replace(url.split('/')[-1], ''), '')

        return book_content

    def to_db(self, url=None):
        if url:
            self.get_book_chapter(url)
        else:
            for i in book_all_list[:50]:
                print(i)
                to_db_data["parts"].clear()
                to_db_data["book_name"] = i["book_name"]
                to_db_data["author"] = i["author"]
                to_db_data["book_url"] = i["book_url"]
                chapter_data = self.get_book_chapter(i["book_url"])
                to_db_data["book_img"] = chapter_data["book_data"]["book_img"]
                to_db_data["book_blurb"] = chapter_data["book_data"]["book_blurb"]
                for chapter_i in chapter_data["chapter_all_list"]:
                    to_db_data["parts"].append({
                        "chapter_name": chapter_i["chapter_name"],
                        "chapter_url": chapter_i["chapter_url"],
                        "chapter_id": get_new_uuid(),
                        "part_content": self.get_book_content(chapter_i["chapter_url"])

                    })
                    logger.info(i["book_name"] + chapter_i["chapter_name"])

                    time.sleep(2)
                    # break

                mongo_client = get_mongo_client()
                col = mongo_client.col_books  # 创建/进入集合
                if not col.find_one({"book_name": to_db_data["book_name"]}):
                    col.insert_one(to_db_data)  # 插入数据
                break


if __name__ == '__main__':
    reptile_client = ReptileClient()
    #
    # for i in range(1, 666):
    #     reptile_client.get_book_data_list(i)

    # with open("data.json", 'w') as f:
    #     f.write(json.dumps(search_all_list))

    print(reptile_client.to_db())
    # print(reptile_client.search_book("灵舟"))
    # print(reptile_client.get_book_chapter("https://www.23dd.cc/du/27/27431/"))
    # print(reptile_client.get_book_content("https://www.23usp.com/xs_718/496377.html"))
