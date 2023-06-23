import datetime

from bson import ObjectId
from flask import Blueprint, request

from gateway.crawl_scripts.dingdian import ReptileClient
from gateway.logger import LogDecorator
from internal.db.mongo.mongo_api import get_mongo_client

bp_books = Blueprint(
    'bp_books',
    __name__,
    url_prefix='/books'
)

mongo_client = get_mongo_client()
col = mongo_client.col_books  # 创建/进入集合


@bp_books.route("", methods=['GET'])
@LogDecorator()
def get_book_data():
    """
    获取全部小说
    :return:
    """

    result_list = list(col.find({"book_name": {"$ne": None}, "book_id": {"$ne": None}}, {"parts": 0, "_id": 0}))

    return result_list


@bp_books.route("/chapters/<book_id>", methods=['GET'])
@LogDecorator()
def get_book_chapters(book_id):
    """
    获取章节目录
    :return:
    """

    result = col.find_one(
        {"book_id": book_id},
        {

            "parts": {

                "$slice": [0, 50],
            },
            "book_name": 1,
            "author": 1,
            "category": 1,
            "book_abstract": 1,
            "last_chapter_id": 1,
            "last_chapter_title": 1,
            "last_chapter_time": 1,
            "word_count": 1,
            "read_count": 1,
            "thumb_url": 1,
            "_id": 0}
    )

    # result = col.find_one(
    #     {"book_id": book_id},
    #     {"parts": {"chapter_content": 0, }, "_id": 0}
    # )

    return result


@bp_books.route("/content/<chapter_id>", methods=['GET'])
@LogDecorator()
def get_chapters_content(chapter_id):
    """
    获取章节内容
    :return:
    """

    result_dict = col.find_one({"parts.chapter_id": chapter_id, "book_id": {"$ne": None}},
                               {"parts": {"$elemMatch": {"chapter_id": chapter_id}}, "book_name": 1})

    if result_dict:
        chapter_content_id = result_dict["parts"][0]["chapter_content"]
        chapter_content = col.find_one({"_id": ObjectId(chapter_content_id)}, {"content_text": 1, "_id": 0})
        result_dict["parts"][0]["chapter_content"] = chapter_content[
            "content_text"] if chapter_content else chapter_content_id

    return result_dict


if __name__ == '__main__':
    ...
    # book_id = "6851451000734092301"
    # result_list = list(col.find({"book_id": book_id}, {"parts": {"chapter_id": 1,"chapter_name":1,"chapter_url":1,}, "_id":0 }))
    # chapter_id = "6851452684927500808"
    # result_dict = col.find_one({"parts.chapter_id": chapter_id}, {"parts": {"chapter_id": 1,"chapter_content":1,"chapter_name":1,"chapter_url":1,"parts.$":1}, "_id":0 })
    # print(result_list)
    # result_list =  col.find_one(
    #         {"book_id": book_id},
    #         {"parts": {"chapter_content": 0}, "_id": 0}
    #     )
    #
    # print(result_list)
    # result_list = list(col.find({"book_name": {"$ne": None}} , {"parts": 0, "_id": 0}))
    # print(result_list)

    # book_id = "6775194486248049678"
    # s_time = datetime.datetime.now()
    # result = col.find_one(
    #     {"book_id": book_id},
    #     {
    #
    #         "parts": {
    #
    #             "$slice": [2, 3],
    #
    #         },
    #
    #         "book_name": 1,
    #         "author": 1,
    #         "category": 1,
    #         "book_abstract": 1,
    #         "last_chapter_id": 1,
    #         "last_chapter_title": 1,
    #         "last_chapter_time": 1,
    #         "word_count": 1,
    #         "read_count": 1,
    #         "thumb_url": 1,
    #         "_id": 0}
    # )
    # print(result)
    # print(datetime.datetime.now() - s_time)

    chapter_id = "7050410575909620769"
    # s_time = datetime.datetime.now()
    result_dict = col.find_one({"parts.chapter_id": chapter_id, "book_id": {"$ne": None}},
                          {"parts": {"$elemMatch": {"chapter_id": chapter_id}}, "book_name": 1,"_id":0})

    if result_dict:
        chapter_content_id = result_dict["parts"][0]["chapter_content"]
        chapter_content = col.find_one({"_id": ObjectId(chapter_content_id)}, {"content_text": 1, "_id": 0})
        result_dict["parts"][0]["chapter_content"] = chapter_content[
            "content_text"] if chapter_content else chapter_content_id
    print(result_dict)
    # # for i in result:
    # #     print(i)
    # print(datetime.datetime.now()-s_time)

    # result_dict = col.find_one({"parts.chapter_id": chapter_id, "book_id": {"$ne": None}}, {
    #     "parts": {
    #         "chapter_id": 1,
    #         "chapter_content": 1,
    #         "chapter_name": 1,
    #         "chapter_url": 1,
    #         "next_chapter_id":1,
    #         "parts.$": 1,
    #
    #     }, "_id": 0})
    # if result_dict:
    #     chapter_content_id = result_dict["parts"][0]["chapter_content"]
    #     chapter_content = col.find_one({"_id": ObjectId(chapter_content_id)}, {"content_text": 1, "_id": 0})
    #     result_dict["parts"][0]["chapter_content"] = chapter_content["content_text"] if chapter_content else chapter_content_id
