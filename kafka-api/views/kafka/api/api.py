from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter
from extensions.utils import *
from fastapi.responses import JSONResponse
from concurrent.futures import ThreadPoolExecutor, as_completed

Mongo = MongoConn(log=False, db='KafkaPro')
router = APIRouter(
    prefix="/api",
    tags=["kafka"],
    default_response_class=ORJSONResponse
)
bootstrap_servers = '172.19.1.209:9092'
topic = 'finance_tax_task_status_demo'


@router.post("/topic/list")
async def Topic_List(item: dict):
    # Kafka集群的连接信息
    try:
        servers = item.get('servers', 'localhost:9092')
        data = KafkaApi(servers=servers).topic_list()
        return JSONResponse(status_code=200, content={"data": data, "status": "success", "msg": "获取topic成功"})
    except Exception as e:
        logger.info(e)
        return JSONResponse(status_code=200, content={"data": [], "status": False, "msg": "连接失败"})


@router.post("/topic/data")
async def Topic_data(item: dict):
    json_data = []
    try:
        servers = item.get('servers')
        topic = item.get('topic')
        topic_num = item.get('topic_num')
        find_item = {
            "servers": servers,
            "topic": topic,
        }
        data = Mongo.findall('topic', find_item,
                             sortfield='timestamp', limit=topic_num)

        for message in data:
            value = message.get("value")
            key = message.get("key")
            json_value = uni_replace(str(value))
            query_dict = {
                "partition": message.get("partition"),
                "offset": message.get("offset"),
                "key": key,
                "id": str(message.get('_id')),
                "value": json_value,
                "timestamp": get_date(message.get("timestamp"))
            }
            json_data.append(query_dict)
    except Exception as e:
        logger.info(e)
    return JSONResponse(status_code=200, content={"data": json_data, "status": "success", "msg": "获取topic成功"})


@router.post("/topic/task")
async def Topic_task(item: dict):
    json_data = []
    try:
        servers = item.get('servers')
        topic = item.get('topic')
        find_item = {
            "servers": servers,
            "topic": topic,
        }
        data = Mongo.findall('topic_task', find_item,
                             sortfield='datetime', limit=100)
        json_data = foomatMid(data) if data else data
    except Exception as e:
        logger.info(e)
    return JSONResponse(status_code=200, content={"data": json_data, "status": "success", "msg": "获取task成功"})


@router.post("/topic/data/task")
async def Topic_task(item: dict):
    try:
        servers = item.get('servers')
        topic_num = item.get('topic_num', 11)
        topic = item.get('topic', 'finance_tax_task_status_test')
        ThreadPoolExecutor(10).submit(topic_task, servers=servers,
                                      topic=topic, topic_num=topic_num)
        # KafkaApi(servers=servers).topic_data(
        # topic_name=topic, topic_num=int(topic_num))
        return JSONResponse(status_code=200, content={"data": [], "status": True, "msg": "send topic task True"})
    except Exception as e:
        logger.info(e)
        logger.error(traceback.format_exc())

        return JSONResponse(status_code=200, content={"data": [], "status": False, "msg": "send topic task False"})


@router.post("/topic/data/search")
async def Topic_search(item: dict):
    json_data = []
    try:
        servers = item.get('servers')
        searchKey = item.get('searchKey')
        topic = item.get('topic', '')
        find_item = {
            "servers": servers,
            "topic": topic,
            "key": {"$regex": '{}'.format(searchKey)}
        }
        data = Mongo.find_query('topic', find_item)
        if not data:
            data = Mongo.find_query('topic',
                                    {
                                        "servers": servers,
                                        "topic": topic,
                                        "value": {"$regex": '{}'.format(searchKey)}
                                    }
                                    )

        for message in data:
            json_value = uni_replace(message.get("value"))
            key = message.get("key")
            query_dict = {
                "partition": message.get("partition"),
                "offset": message.get("offset"),
                "id": str(message.get('_id')),
                "key": key,
                "value": json_value,
                "timestamp": get_date(message.get("timestamp"))
            }
            json_data.append(query_dict)
    except Exception as e:
        logger.info(e)
    return JSONResponse(status_code=200, content={"data": json_data, "status": "success", "msg": "获取topic成功"})


@router.post("/topic/data/model")
async def Topic_model(item: dict):
    json_data = []
    try:
        _id = item.get('id')

        find_item = {
            "_id": ObjectId(_id),
        }
        data = Mongo.find_query('topic_data', find_item)

        for message in data:
            value = message.get("value")
            try:
                base_value = base64.b64decode(value)
                value = gzip.decompress(base_value).decode()
            except:
                try:
                    value = gzip.decompress(value).decode()
                except:
                    value = value.decode()

            json_value = uni_replace(value)
            key = message.get("key")
            json_data = {
                "partition": message.get("partition"),
                "offset": message.get("offset"),
                "key": key,
                "value": json_value,
                "timestamp": get_date(message.get("timestamp"))
            }
    except Exception as e:
        logger.info(e)
    return JSONResponse(status_code=200, content={"data": json_data, "status": "success", "msg": "获取topic成功"})


@router.post("/consumer/add")
async def Consumer_add(item: dict):
    dt = datetime.datetime.now()
    kafkaServe = item.get('kafkaServe')
    kafkaName = item.get('kafkaName')
    query = {
        "kafkaServe": kafkaServe,
        "kafkaName": kafkaName,
    }
    if Mongo.find_query('consumer', query):
        return JSONResponse(status_code=200, content={"status": False, "msg": "已存在"})
    else:

        query.update({"datetime": str(dt)})
        Mongo.insert('consumer', query)
        return JSONResponse(status_code=200, content={"status": True, "msg": "创建成功"})


@router.post("/consumer/edit")
async def Consumer_edit(item: dict):
    dt = datetime.datetime.now()
    try:
        item = item.get('old')
        id = item.get('_id')
        item_dict = {
            '_id': ObjectId(id),
        }
        new = item
        new['_id'] = ObjectId(id)
        new.update({"updatetime": str(dt)})
        print(item_dict)
        print(new)
        Mongo.update_many('consumer', filter=item_dict,
                          data=new)
        return JSONResponse(status_code=200, content={"status": True, "msg": "修改成功"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={"status": False, "msg": "修改失败"})


@router.post("/consumer/data")
async def Consumer_data(item: dict):
    query = Mongo.findall('consumer')
    query = foomatMid(query)
    return JSONResponse(status_code=200, content={"data": query, "status": True, "msg": "获取consumer成功"})


@router.post("/consumer/test")
async def Consumer_test(item: dict):
    kafkaServe = item.get('kafkaServe')
    kafkaName = item.get('kafkaName')
    item_dict = {
        'kafkaServe': kafkaServe,
        'kafkaName': kafkaName,
    }
    try:
        data = KafkaApi(servers=kafkaServe).topic_list()
        Mongo.update_one('consumer', filter=item_dict,
                         data={"topic": len(data)})
        return JSONResponse(status_code=200, content={"status": True, "msg": "测试连接成功"})
    except Exception as e:
        logger.info(e)
        Mongo.update_one('consumer', filter=item_dict,
                         data={"topic": None})
        return JSONResponse(status_code=200, content={"status": False, "msg": "测试连接失败"})


@router.post("/consumer/del")
async def Consumer_del(item: dict):
    kafkaServe = item.get('kafkaServe')
    kafkaName = item.get('kafkaName')
    query = {
        "kafkaServe": kafkaServe,
        "kafkaName": kafkaName,
    }
    try:
        Mongo.delete_query('consumer', query)
        return JSONResponse(status_code=200, content={"status": True, "msg": "删除成功"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={"status": False, "msg": "删除失败"})
