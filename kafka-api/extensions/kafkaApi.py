from .mongoApi import *
from kafka import TopicPartition, KafkaAdminClient, KafkaConsumer
import gzip
import base64

MonConn = MongoConn(log=False, db='KafkaPro')


def delid_list(item):
    result = []
    for num, i in enumerate(item):
        i.update({'_id': num + 1})
        result.append(i)
    return result


class KafkaApi:
    def __init__(self, servers, auto_offset_reset='earliest') -> None:
        # 创建KafkaAdminClient实例
        self.servers = servers
        self.Adminclient = KafkaAdminClient(
            bootstrap_servers=servers)
        self.consumer = KafkaConsumer(
            bootstrap_servers=servers, auto_offset_reset=auto_offset_reset,
            consumer_timeout_ms=10000)
        self.collect = 'topic'
        self.collect_data = 'topic_data'
        # self.p = Pool(10)

    def topic_list(self):
        # 获取Kafka集群中的所有主题
        topic_list = []
        all_topics = self.Adminclient.list_topics()
        for top in all_topics:
            topic_list.append(
                {'topic': top}
            )

        return topic_list

    def topic_data(self, topic_name, topic_num=11):
        partitions = list(self.consumer.partitions_for_topic(topic_name))
        # 打印分区数量
        task_item = {
            "topic_num": topic_num,
            "servers": self.servers,
            "topic": topic_name,
            "datetime": str(datetime.datetime.now())
        }
        task_id = MonConn.insert('topic_task', task_item)
        for part in partitions:
            self.thread_part(part=part, topic_name=topic_name,
                             topic_num=topic_num)
        MonConn.delete('topic_task', task_id)

    def thread_part(self, part, topic_name, topic_num):
        try:
            tp = TopicPartition(topic_name, part)
            # 获取当前分区的最大偏移量
            end_offset = self.consumer.end_offsets([tp])[tp] - 1
            tp = TopicPartition(topic_name, part)
            self.consumer.assign([tp])
            seek_num = end_offset - topic_num
            seek_num = 0 if seek_num < 0 else seek_num
            self.consumer.seek(TopicPartition(
                topic_name, part), seek_num)

            for message in self.consumer:
                offset = message.offset
                partition = message.partition
                timestamp = message.timestamp
                key = message.key
                value = message.value
                data_value = value
                try:
                    key = key.decode()
                except:
                    pass
                try:
                    base_value = base64.b64decode(value)
                    data_value = gzip.decompress(base_value).decode()
                except:
                    try:
                        data_value = gzip.decompress(value).decode()
                    except:
                        try:
                            data_value = value.decode()
                        except:
                            data_value = value

                item = {
                    "partition": partition,
                    "offset": offset,
                    "servers": self.servers,
                    "topic": topic_name,
                    "key": key,
                    "value": data_value[:200] + '\n......\n' + data_value[-200:] if data_value else data_value,
                    "timestamp": timestamp,
                }
                # 去重
                dep_item = {
                    "partition": partition,
                    "offset": offset,
                    "servers": self.servers,
                    "topic": topic_name,
                }
                find_query = MonConn.find_query(self.collect, dep_item)
                if find_query:
                    pass
                else:
                    inserted_id = MonConn.insert(self.collect, item)

                    item.update({
                        "value": value,
                        "_id": inserted_id,
                    })
                    MonConn.insert(self.collect_data, item)

                if offset >= end_offset:
                    break
        except Exception as e:
            print(e)

    def partition(self, topic):
        topic_name = topic
        topic_list = []
        topic_info = self.Adminclient.describe_topics(topics=[topic_name])
        for topics in topic_info:
            partitions = topics.get('partitions')
            for partition_dict in partitions:
                partition = partition_dict.get('partition')
                topic_list.append(partition)
        topic_list.sort()
        return topic_list


if __name__ == '__main__':
    topic_name = 'finance_tax_task_status_test'
    topic = 'finance_tax_test'
    # Kafka集群的连接信息
    bootstrap_servers = '172.19.1.209:9092'
    data = KafkaApi(servers=bootstrap_servers).topic_data(topic)
    print(data)
