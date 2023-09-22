import re
import gzip
import traceback
import unicodedata
import json
import base64
import datetime
from extensions.mongoApi import *
from extensions.kafkaApi import *
from extensions.mysqlApi import *
from logs.settings import logger
from bson import ObjectId


def foomatMid(result):
    result_list = []
    for res in result:
        _id = res['_id']
        res['_id'] = str(_id)
        result_list.append(res)
    return result_list


def get_date(item):
    return str(datetime.datetime.fromtimestamp(int(item) / 1000))


def uni_replace(item):
    result = re.sub(
        r"(\\u[a-zA-Z0-9]{4})",
        lambda x: x.group(1).encode("utf-8").decode("unicode-escape"),
        item,
    )
    result = re.sub(r"(\\r|\\n|\\t|\xa0|\\u[0-9]{4})", lambda x: "", result)
    result = unicodedata.normalize("NFKC", result)
    return result.strip()


def delid(item):
    if isinstance(item, list):
        item = item[0]
    del item['_id']
    return item


def delid_list(item):
    result = []
    for num, i in enumerate(item):
        i.update({'_id': str(num + 1)})
        result.append(i)
    return result


def topic_task(servers=None, topic=None, topic_num=None):
    try:
        KafkaApi(servers=servers).topic_data(
            topic_name=topic, topic_num=int(topic_num))
    except Exception as e:
        print(e)
