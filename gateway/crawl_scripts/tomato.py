import datetime
import time

import requests
from lxml import etree
from gateway.crawl_scripts.to_db_data_const import to_db_data
from gateway.utils.params_check import is_json
from internal.common.gen_random_obj import get_new_uuid
from internal.db.mongo.mongo_api import get_mongo_client
from utils.date_time_utils import timestamp_to_time
from utils.logger import setup_log

logger = setup_log('crawl_scripts')

search_all_list = []


def get_font_map():
    """
    获取字体映射关系
    :return:
    """

    font_utf_8 = ['D', '在', '主', '特', '家', '军', '然', '表', '场', '4', '要', '只', 'v', '和', '6', '别', '还', 'g',
                  '现',
                  '儿', '岁', '此', '象', '月', '3', '出', '战', '工', '相', 'o', '男', '直', '失', '世', 'F', '都',
                  '平', '文',
                  '什', 'V', 'O', '将', '真', 'T', '那', '当', '会', '立', '些', 'u', '是', '十', '张', '学', '气',
                  '大', '爱',
                  '两', '命', '全', '后', '东', '性', '通', '被', '1', '它', '乐', '接', '而', '感', '车', '山', '公',
                  '了',
                  '常', '以', '何', '可', '话', '先', 'p', 'i', '叫', '轻', 'M', '士', 'w', '着', '变', '尔', '快', 'l',
                  '个',
                  '说', '少', '色', '里', '安', '花', '远', '7', '难', '师', '放', 't', '报', '认', '面', '道', 'S',
                  '克', '地',
                  '度', 'I', '好', '机', 'U', '民', '写', '把', '万', '同', '水', '新', '没', '书', '电', '吃', '像',
                  '斯', '5',
                  '为', 'y', '白', '几', '日', '教', '看', '但', '第', '加', '候', '作', '上', '拉', '住', '有', '法',
                  'r', '事',
                  '应', '位', '利', '你', '声', '身', '国', '问', '马', '女', '他', 'Y', '比', '父', 'x', 'A', 'H', 'N',
                  's',
                  'X', '边', '美', '对', '所', '金', '活', '回', '意', '到', 'z', '从', 'j', '知', '又', '内', '因',
                  '点', 'Q',
                  '三', '定', '8', 'R', 'b', '正', '或', '夫', '向', '德', '听', '更', '得', '告', '并', '本', 'q',
                  '过', '记',
                  'L', '让', '打', 'f', '人', '就', '者', '去', '原', '满', '体', '做', '经', 'K', '走', '如', '孩',
                  'c', 'G',
                  '给', '使', '物', '最', '笑', '部', '员', '等', '受', 'k', '行', '一', '条', '果', '动', '光', '门',
                  '头',
                  '见', '往', '自', '解', '成', '处', '天', '能', '于', '名', '其', '发', '总', '母', '的', '死', '手',
                  '入',
                  '路', '进', '心', '来', 'h', '时', '力', '多', '开', '已', '许', 'd', '至', '由', '很', '界', 'n',
                  '小', '与',
                  'Z', '想', '代', '么', '分', '生', '口', '再', '妈', '望', '次', '西', '风', '种', '带', 'J', '实',
                  '情', '才',
                  '这', 'E', '我', '神', '格', '长', '觉', '间', '年', '眼', '无', '不', '亲', '关', '结', '0', '友',
                  '信', '下',
                  '却', '重', '己', '老', '2', '音', '字', 'm', '呢', '明', '之', '前', '高', 'P', 'B', '目', '太', 'e',
                  '9',
                  '起', '稜', '她', '也', 'W', '用', '方', '子', '英', '每', '理', '便', '四', '数', '期', '中', 'C',
                  '外', '样',
                  'a', '海', '们', '任']
    font_unicode = ['gid58344', 'gid58345', 'gid58346', 'gid58347', 'gid58348', 'gid58349', 'gid58350', 'gid58351',
                    'gid58352',
                    'gid58353', 'gid58354', 'gid58355', 'gid58356', 'gid58357', 'gid58359', 'gid58360', 'gid58361',
                    'gid58362',
                    'gid58363', 'gid58364', 'gid58365', 'gid58368', 'gid58369', 'gid58370', 'gid58371', 'gid58372',
                    'gid58373',
                    'gid58374', 'gid58375', 'gid58376', 'gid58377', 'gid58378', 'gid58379', 'gid58380', 'gid58381',
                    'gid58382',
                    'gid58383', 'gid58384', 'gid58385', 'gid58386', 'gid58387', 'gid58388', 'gid58389', 'gid58390',
                    'gid58391',
                    'gid58392', 'gid58394', 'gid58395', 'gid58396', 'gid58397', 'gid58398', 'gid58399', 'gid58400',
                    'gid58401',
                    'gid58402', 'gid58403', 'gid58404', 'gid58405', 'gid58406', 'gid58407', 'gid58408', 'gid58409',
                    'gid58410',
                    'gid58411', 'gid58412', 'gid58413', 'gid58414', 'gid58415', 'gid58416', 'gid58417', 'gid58418',
                    'gid58419',
                    'gid58420', 'gid58421', 'gid58422', 'gid58423', 'gid58424', 'gid58425', 'gid58426', 'gid58427',
                    'gid58428',
                    'gid58429', 'gid58430', 'gid58431', 'gid58432', 'gid58433', 'gid58434', 'gid58435', 'gid58436',
                    'gid58437',
                    'gid58438', 'gid58439', 'gid58440', 'gid58441', 'gid58442', 'gid58443', 'gid58444', 'gid58445',
                    'gid58446',
                    'gid58447', 'gid58448', 'gid58449', 'gid58450', 'gid58451', 'gid58452', 'gid58453', 'gid58454',
                    'gid58455',
                    'gid58456', 'gid58457', 'gid58458', 'gid58460', 'gid58461', 'gid58462', 'gid58463', 'gid58464',
                    'gid58465',
                    'gid58466', 'gid58467', 'gid58468', 'gid58469', 'gid58470', 'gid58471', 'gid58472', 'gid58473',
                    'gid58474',
                    'gid58475', 'gid58476', 'gid58477', 'gid58478', 'gid58479', 'gid58480', 'gid58481', 'gid58482',
                    'gid58483',
                    'gid58484', 'gid58485', 'gid58486', 'gid58487', 'gid58488', 'gid58489', 'gid58490', 'gid58491',
                    'gid58492',
                    'gid58493', 'gid58494', 'gid58495', 'gid58496', 'gid58497', 'gid58498', 'gid58499', 'gid58500',
                    'gid58501',
                    'gid58502', 'gid58503', 'gid58504', 'gid58505', 'gid58506', 'gid58507', 'gid58508', 'gid58509',
                    'gid58510',
                    'gid58511', 'gid58512', 'gid58513', 'gid58514', 'gid58515', 'gid58516', 'gid58517', 'gid58518',
                    'gid58519',
                    'gid58520', 'gid58521', 'gid58522', 'gid58523', 'gid58524', 'gid58525', 'gid58526', 'gid58527',
                    'gid58528',
                    'gid58529', 'gid58530', 'gid58531', 'gid58532', 'gid58533', 'gid58534', 'gid58535', 'gid58536',
                    'gid58537',
                    'gid58538', 'gid58539', 'gid58540', 'gid58541', 'gid58542', 'gid58543', 'gid58544', 'gid58545',
                    'gid58546',
                    'gid58547', 'gid58548', 'gid58549', 'gid58551', 'gid58552', 'gid58553', 'gid58554', 'gid58555',
                    'gid58556',
                    'gid58557', 'gid58558', 'gid58559', 'gid58560', 'gid58561', 'gid58562', 'gid58563', 'gid58564',
                    'gid58565',
                    'gid58566', 'gid58567', 'gid58568', 'gid58569', 'gid58570', 'gid58571', 'gid58572', 'gid58573',
                    'gid58574',
                    'gid58575', 'gid58576', 'gid58577', 'gid58578', 'gid58579', 'gid58581', 'gid58582', 'gid58583',
                    'gid58585',
                    'gid58586', 'gid58587', 'gid58588', 'gid58589', 'gid58590', 'gid58591', 'gid58592', 'gid58593',
                    'gid58594',
                    'gid58595', 'gid58596', 'gid58597', 'gid58598', 'gid58599', 'gid58600', 'gid58601', 'gid58602',
                    'gid58603',
                    'gid58604', 'gid58605', 'gid58606', 'gid58607', 'gid58608', 'gid58609', 'gid58610', 'gid58611',
                    'gid58612',
                    'gid58613', 'gid58614', 'gid58615', 'gid58616', 'gid58617', 'gid58618', 'gid58619', 'gid58620',
                    'gid58621',
                    'gid58622', 'gid58623', 'gid58624', 'gid58625', 'gid58626', 'gid58627', 'gid58628', 'gid58629',
                    'gid58630',
                    'gid58631', 'gid58632', 'gid58633', 'gid58634', 'gid58635', 'gid58636', 'gid58637', 'gid58638',
                    'gid58639',
                    'gid58640', 'gid58641', 'gid58642', 'gid58643', 'gid58644', 'gid58645', 'gid58646', 'gid58647',
                    'gid58648',
                    'gid58649', 'gid58651', 'gid58652', 'gid58653', 'gid58654', 'gid58656', 'gid58657', 'gid58658',
                    'gid58659',
                    'gid58660', 'gid58661', 'gid58662', 'gid58663', 'gid58664', 'gid58665', 'gid58666', 'gid58667',
                    'gid58668',
                    'gid58669', 'gid58670', 'gid58671', 'gid58672', 'gid58673', 'gid58674', 'gid58675', 'gid58676',
                    'gid58677',
                    'gid58678', 'gid58679', 'gid58680', 'gid58681', 'gid58682', 'gid58683', 'gid58684', 'gid58685',
                    'gid58686',
                    'gid58687', 'gid58688', 'gid58689', 'gid58690', 'gid58691', 'gid58692', 'gid58693', 'gid58694',
                    'gid58695',
                    'gid58696', 'gid58697', 'gid58698', 'gid58699', 'gid58700', 'gid58701', 'gid58702', 'gid58703',
                    'gid58704',
                    'gid58705', 'gid58706', 'gid58707', 'gid58708', 'gid58709', 'gid58710', 'gid58711', 'gid58712',
                    'gid58713',
                    'gid58714', 'gid58715']

    # 十进制转16进制
    font_unicode = [str(hex(int(v.replace("gid", "")))).replace("0x", r"\u") for v in font_unicode]

    return dict(zip(font_unicode, font_utf_8))


font_map_dict = get_font_map()
mongo_client = get_mongo_client()


class ReptileClient:
    def __init__(self):
        self.url = "https://fanqienovel.com"
        self.search_url = "https://fanqienovel.com/api/author/search/search_book/v1"
        self.chapter_url = "https://fanqienovel.com/page/"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/108.0.0.0 Safari/537.36",
        }

        self.proxies = {
            'http': '127.0.0.1:7890',
            'https': '127.0.0.1:7890'
        }
        self.cookies = {
            'Hm_lvt_2667d29c8e792e6fa9182c20a3013175': '1694597640',
            'csrf_session_id': 'c3f63de44a0cf8b17aa54ce9ad26ee9f',
            's_v_web_id': 'verify_lmhjojva_a3VciEOn_yTaU_4ILV_8eN6_lSfp8VAcHAAX',
            'novel_web_id': '7236769868573804066',
            'passport_csrf_token': '9b36a035a5c7661157c3b0a1c1640e14',
            'passport_csrf_token_default': '9b36a035a5c7661157c3b0a1c1640e14',
            'odin_tt': '7a101fd27a531827ccc49f1e07f8c69584f7056dc08499318141826a0ff3077910e9b259c2e9dae290a7a10af4bb0abc',
            'n_mh': 'NCNPUY4KobWicisVMLB1U3djIl6v8SCci-lihMuAu3c',
            'sid_guard': 'a38c86452d13928110d8695db9140573%7C1694598176%7C5184000%7CSun%2C+12-Nov-2023+09%3A42%3A56+GMT',
            'uid_tt': '59c2ede8bc2a9261f5b5dde5df7b896c',
            'uid_tt_ss': '59c2ede8bc2a9261f5b5dde5df7b896c',
            'sid_tt': 'a38c86452d13928110d8695db9140573',
            'sessionid': 'a38c86452d13928110d8695db9140573',
            'sessionid_ss': 'a38c86452d13928110d8695db9140573',
            'sid_ucp_v1': '1.0.0-KGFmNzZiMDZhZmEzMTg2ODY4YmFlODRmODgwYTczNmFhOGI0MjljODkKHQj269T33wIQoIiGqAYYxxMgDDDlju7UBTgHQPQHGgJscSIgYTM4Yzg2NDUyZDEzOTI4MTEwZDg2OTVkYjkxNDA1NzM',
            'ssid_ucp_v1': '1.0.0-KGFmNzZiMDZhZmEzMTg2ODY4YmFlODRmODgwYTczNmFhOGI0MjljODkKHQj269T33wIQoIiGqAYYxxMgDDDlju7UBTgHQPQHGgJscSIgYTM4Yzg2NDUyZDEzOTI4MTEwZDg2OTVkYjkxNDA1NzM',
            'store-region': 'jp',
            'store-region-src': 'uid',
            'ttwid': '1%7C11fhLuzlgqEMdF8lfDq92K7si8LO9nXz59Hs5AExPfI%7C1694598189%7C8213ba55ef9811b5758e4fb6293550fbedeac1d760d0c5e7058117a1e7bdddd2',
            'msToken': 'ZsWgeM9aK48w4DwULdameRg9Bre1kBGnKfWt9YFz1RfdZPCfw6ijiXFkW33IKfyrJ3DDLhx5ginRMOus82hVrv68afdcpHTGXrL2wO_ffT8QEWRX586MJVi3fzINIUw=',
            'Hm_lpvt_2667d29c8e792e6fa9182c20a3013175': '1694598182',
        }
        self.col = mongo_client.col_books  # 创建/进入集合

    def get_response_data(self, url, data=None, params=None, result_type="json"):
        """
        :param url:
        :param data:
        :param params:
        :param result_type:
        :return:
        """

        s_time = datetime.datetime.now()
        response = requests.get(url=url, data=data, params=params, headers=self.headers, cookies=self.cookies)

        logger.info(f"url:{url}\nstatus_code:{response.status_code}\nTime Used:{datetime.datetime.now() - s_time}")

        if result_type == "json":
            if response.status_code != 200 or not is_json(response.text):
                logger.error(
                    f"url:{url}\ndata:{data}\nparams:{params}\n" + response.text +
                    f"\n{datetime.datetime.now() - s_time}")
                raise Exception("get error!!!")
            return response.json()
        elif result_type == "text":
            if response.status_code != 200 or is_json(response.text):
                logger.error(
                    f"url:{url}\ndata:{data}\nparams:{params}\n" +
                    response.text + f"\n{datetime.datetime.now() - s_time}")
                raise Exception("get error!!!")
            return response.text

    def search_book(self, book_name):
        """
        搜索书名是否存在,自定义筛选入库
        :param book_name:
        :return:
        """

        page_text = self.get_response_data(self.search_url, params={
            "filter": "127,127,127,127",
            "page_count": 10,
            "page_index": 0,
            "query_type": 0,
            "query_word": book_name
        }, result_type="json")

        if self.col.find_one({"book_name": book_name}, {"book_id": 1}):
            return
        for i in page_text.get("data").get("search_book_data_list"):
            self.to_db(i)

            break
            # if i["author"] == "九当家":
            #     self.to_db(i)
            #     break

        return page_text

    @staticmethod
    def download_img(img_url, new_book_id):
        response = requests.get(img_url)

        with open(f"../static/{new_book_id}.png", 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return f"/static/{new_book_id}.png"

    def get_book_chapter(self, book_id):
        """
        获取简介,图书封面,章节名,url地址
        :param book_id:
        :return:
        """
        response = self.get_response_data(f"{self.chapter_url}{book_id}", result_type="text")
        # print(response)
        tree = etree.HTML(response)
        chapter_all_list = []

        text_list = tree.xpath(f"//div[@class='chapter']//text()")
        href_list = tree.xpath(f"//div[@class='chapter']//@href")
        href_list = [self.url + i for i in href_list]

        text_href_list = list(zip(text_list, href_list))

        return text_href_list

    def get_book_content(self, url, book_name, author):
        """
        获取章节内容
        :param author:
        :param book_name:
        :param url:
        :return:
        """

        response = self.get_response_data(url, result_type="text")
        tree = etree.HTML(response)
        content_text = tree.xpath(f"//*[@id='app']/div/div/div/div[2]//text()")
        # book_name = tree.xpath("//*[@id='app']/div/div/div/div[3]/div[1]/span[1]/a//text()")
        # author = tree.xpath("//*[@id='app']/div/div/div/div[3]/div[1]/span[2]/a//text()")
        # chapters_word_count = tree.xpath("//*[@id='app']/div/div/div/div[3]/div[1]/span[3]/text()[1]")
        last_chapter_time = tree.xpath("//*[@id='app']/div/div/div/div[3]/div[1]/span[4]/text()")

        new_content_text = []
        for c_i in content_text:
            for f_i in font_map_dict:
                if f_i in c_i.encode("unicode_escape").decode("utf-8"):
                    c_i = c_i.encode("unicode_escape").decode("utf-8").replace(f_i, font_map_dict[f_i].encode(
                        "unicode_escape").decode("utf-8")).encode("utf-8").decode("unicode_escape")

            new_content_text.append(c_i)

        content_text = "\n  ".join(new_content_text).replace("上一章", "").replace("下一章", "")

        result_dict = {
            "book_name": book_name,
            "author": author,
            "chapters_word_count": len(content_text),
            "last_chapter_time": last_chapter_time[0] if last_chapter_time else "",
            "content_text": content_text,
        }

        return result_dict

    def add_chapter_content(self, book_id, book_name, author):
        """
        添加每一章节的内容
        :param author:
        :param book_id:
        :param book_name:
        :return:
        """
        text_href_list = self.get_book_chapter(book_id)

        for index, t_h in enumerate(text_href_list):
            book_data = self.col.find_one({"parts.chapter_name": t_h[0]}, {"book_id": 1})
            if not book_data:
                result_dict = self.get_book_content(t_h[1], book_name, author)
                chapter_id = t_h[1].split("/")[-1]
                content_text_id = self.col.insert_one({
                    "content_text": result_dict["content_text"],
                    "chapter_id": chapter_id,
                    "book_name": result_dict["book_name"],
                    "author": result_dict["author"],
                    "type": "content",
                }).inserted_id
                parts_data = {
                    "$addToSet": {"parts": {
                        "chapter_id": chapter_id,
                        "next_chapter_id": chapter_id if index == len(text_href_list) - 1 else
                        text_href_list[index + 1][1].split("/")[-1],
                        "chapter_name": t_h[0],
                        "chapter_url": t_h[1],
                        "book_name": result_dict["book_name"],
                        "author": result_dict["author"],
                        "chapters_word_count": result_dict["chapters_word_count"],
                        "last_chapter_time": result_dict["last_chapter_time"],
                        "chapter_content": str(content_text_id),

                    }}  # 是向数组对象中添加元素和值，操作对象必须为数组类型的字段
                }
                # print(parts_data)
                self.col.update_one(
                    {"book_name": book_name}, parts_data)
                time.sleep(1)

    def to_db(self, data=None):
        if self.col.find_one({"book_name": to_db_data["book_name"]}):
            return
        new_book_id = get_new_uuid()
        data["thumb_url"] = self.download_img(data["thumb_url"], new_book_id)
        to_db_data["parts"].clear()
        to_db_data["book_id"] = data["book_id"]
        to_db_data["new_book_id"] = new_book_id
        to_db_data["book_name"] = data["book_name"]
        to_db_data["thumb_url"] = data["thumb_url"]
        to_db_data["author"] = data["author"]
        to_db_data["category"] = data["category"]
        to_db_data["creation_status"] = data["creation_status"]
        to_db_data["word_count"] = data["word_count"]
        to_db_data["read_count"] = data["read_count"]
        to_db_data["last_chapter_title"] = data["last_chapter_title"]
        to_db_data["last_chapter_time"] = timestamp_to_time(data["last_chapter_time"])
        to_db_data["last_chapter_id"] = data["last_chapter_id"]
        to_db_data["book_abstract"] = data["book_abstract"]
        to_db_data["first_chapter_id"] = data["first_chapter_id"]
        to_db_data["type"] = "details"
        # print(to_db_data)
        self.col.insert_one(to_db_data)  # 插入数据


if __name__ == '__main__':
    reptile_client = ReptileClient()
    #
    # for i in range(1, 666):
    #     reptile_client.get_book_data_list(i)

    # with open("data.json", 'w') as f:
    #     f.write(json.dumps(search_all_list))

    # print(reptile_client.search_book('汽包'))
    # reptile_client.add_chapter_content("6569997542090607620", "灵舟")

    # print(reptile_client.search_book("天域丹尊"))
    # print(reptile_client.add_chapter_content("6851451000734092301", "理想国"))
    # print(reptile_client.get_book_chapter("7177580416302337082"))

    # print(reptile_client.search_book("天域丹尊"))
    # reptile_client.add_chapter_content("6775194486248049678", "天域丹尊")
    # print(reptile_client.get_book_content("https://fanqienovel.com/reader/6775234172882518535"))

    print(reptile_client.search_book('理想国'))
    reptile_client.add_chapter_content("7124986336406146062", "理想国", "柏拉图")

    # print(reptile_client.search_book('弃猫 当我谈起父亲时'))
    # reptile_client.add_chapter_content("7050408665831984136", "弃猫 当我谈起父亲时", "（日）村上春树")

    # print(reptile_client.search_book('理想国'))
    # reptile_client.add_chapter_content("7124986336406146062", "理想国")

    # 搜索模糊匹配
