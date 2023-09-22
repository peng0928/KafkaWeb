import pymongo
import datetime
from loguru import logger as MonLog
from bson.objectid import ObjectId


class Log():

    def __init__(self, log=True):
        self.log = log

    def info(self, msg):
        if self.log:
            MonLog.info(msg)

    def warning(self, msg):
        if self.log:
            MonLog.warning(msg)

    def success(self, msg):
        if self.log:
            MonLog.success(msg)

    def error(self, msg):
        if self.log:
            MonLog.error(msg)

    def debug(self, msg):
        if self.log:
            MonLog.debug(msg)

    def exception(self, msg):
        if self.log:
            MonLog.exception(msg)


class MongoConn:
    def __init__(self, host='localhost', port='27017', db='MongoTest', log=True):
        self.myclient = pymongo.MongoClient(f"mongodb://{host}:{port}/")
        self.mydb = self.myclient[db]
        self.Mlog = Log(log=log)
        self.Mlog.success('Mongodb连接成功')

    def exist_db(self, db):
        msg = '数据库:{} {}存在'
        dblist = self.myclient.list_database_names()
        if str(db) in dblist:
            self.Mlog.info(msg.format(db, ''))
            return True
        else:
            self.Mlog.info(msg.format(db, '不'))
            return False

    def exist_collection(self, collection):
        msg = '数据库:{} {}存在'
        collist = self.mydb.list_collection_names()
        if collection in collist:  # 判断 sites 集合是否存在
            self.Mlog.info(msg.format(collection, ''))
            return True
        else:
            self.Mlog.info(msg.format(collection, '不'))
            return False

    def create(self, collection):
        self.mydb[collection]
        self.Mlog.success(f'{collection} 集合创建成功')

    def insert(self, collection, mydict):
        try:
            mycol = self.mydb[collection]
            result = mycol.insert_one(mydict)
            self.Mlog.success(
                f'数据插入成功 -> Data: {mydict} collection: {collection}')
            inserted_id = result.inserted_id
            return inserted_id
        except Exception as e:
            print(e)
            return None

    def insert_many(self, collection, mylist):
        mycol = self.mydb[collection]
        result = mycol.insert_many(mylist)
        self.Mlog.success(f'数据插入成功 -> Data: {result} collection: {collection}')

    def find(self, collection):
        mycol = self.mydb[collection]
        result = mycol.find_one()
        self.Mlog.success(f'数据查询成功 -> Data: {result} collection: {collection}')
        return result

    def delete(self, collection, ids):
        query = {"_id": ObjectId(ids)}
        mycol = self.mydb[collection]
        mycol.delete_one(query)
        self.Mlog.success(f'数据删除成功 ->%s' % ids)
        return None

    def delete_query(self, collection, query):
        mycol = self.mydb[collection]
        mycol.delete_many(query)
        self.Mlog.success(f'数据删除成功 ->%s' % query)
        return None

    def findall(self, collection, condition: dict = {}, sortfield="time", limit=10):
        result_list = []
        mycol = self.mydb[collection]
        result = mycol.find(condition).sort(sortfield, -1).limit(limit)
        for res in result:
            result_list.append(res)
        self.Mlog.success(
            f'数据查询成功 -> Data: {result_list} collection: {collection}')
        return result_list

    def find_id(self, collection, ids: str):
        mycol = self.mydb[collection]
        result = mycol.find({"_id": ObjectId(ids)})
        result = list(result)
        self.Mlog.success(f'数据查询成功 -> Data: {result} collection: {collection}')
        return result

    def update_one(self, collection, filter, data):
        try:
            mycol = self.mydb[collection]
            query = {'$set': data}
            mycol.update_one(filter, query)
            self.Mlog.success(f'数据更新成功 -> filter: {filter} query: {query}')
            return True
        except Exception as e:
            print(e)
            return False

    def update_many(self, collection, filter, data):
        try:
            mycol = self.mydb[collection]
            query = {'$set': data}
            mycol.update_many(filter, query)
            self.Mlog.success(f'数据更新成功 -> filter: {filter} query: {query}')
            return True
        except Exception as e:
            print(e)
            return False

    def find_query(self, collection, find_query, sort_field=None, sort_order=None, log=False):
        mycol = self.mydb[collection]
        result = mycol.find(find_query)
        result.sort(sort_field, sort_order) if sort_field else result
        result = list(result)
        if log:
            self.Mlog.success(
                f'数据查询成功 -> Data: {result} collection: {collection}')
        return result


if __name__ == '__main__':
    result = MongoConn(db='apitools', log=False).find_id(
        'data', '64ab5511c61219f534722feb')
    for item in result:
        _item = {
            '_id': str(item.get('_id')),
            'code': item.get('code'),
            'time': str(item.get('time')),
        }
        print(_item)
    # MongoConn().insert_collection('penr', {"name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com"})
