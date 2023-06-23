import pymongo
from configurations import config


def get_mongo_client():
    return MongoAPI(
        host=config.get('mongo', 'host'),
        port=config.get('mongo', 'port'),
        user=config.get('mongo', 'user'),
        password=config.get('mongo', 'pass'),
        name=config.get('mongo', 'name')
    )


class MongoAPI(object):

    def __init__(self, host='127.0.0.1', port=27017, user=None, password=None, name=None):
        uri = f"mongodb://{host}:{port}"
        if user and password:
            uri = f"mongodb://{user}:{password}@{host}:{port}"
        if name:
            uri = f"{uri}/{name}"
        self.__client = pymongo.MongoClient(uri)
        self.__db = self.__client[name]

    @property
    def db(self):
        return self.__db

    def get_collection(self):
        return self.__db

    def __getattr__(self, item):
        if item.startswith('col_'):
            return getattr(self.__db, item[4:])
        raise AttributeError


if __name__ == '__main__':
    mongo_client = get_mongo_client()
    col = mongo_client.col_books       # 创建/进入集合
    data = {
        "book_name": "灵舟",
        "author": "无敌贱客",
        "book_url": "",
        "reads": 0,             # 阅读人数
        "parts": [
            {
                'chapter_name': '第一章 一个天下最美、最狠的女人',
                'chapter_url': 'https://www.23usp.com/xs_718/496377.html',
                'chapter_id': "111",
                "part_content": "xxxxxxxxxxxxxxxx"
             },
        ],            # 章节

        "collect": [],          # 收藏
        "blurb": "",            # 简介
        "book_img": "",         # 书籍封面
        "book_number": "",      # 书籍字数
        "book_types": "",       # 书籍类型
        "score": "",            # 书籍评分
    }

    # col.insert_one(data)        # 插入数据

    # parts_data = {
    #     "$addToSet": {"parts": {"xx1": "ss2"}}      # 是向数组对象中添加元素和值，操作对象必须为数组类型的字段
    # }
    #
    # workflow2 = col.update_one(
    #     {"book_name": "灵舟"}, parts_data)
    # print(workflow2)

    query = col.find_one({"parts.chapter_name": "第一千一百五十章 此岸，彼岸（大结局）"}, {"book_id": 1})
    print(query)
    # for i in query:
    #     print(i)
