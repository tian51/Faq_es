# -*- encoding: utf-8 -*-
"""
@File    : es_tool.py
@Time    : 2020/9/5
@Author  : tyz
@Email   : 1239233794@qq.com
@Software: PyCharm
@desc    :
"""
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, parallel_bulk

from data_process import get_datas, get_result


class ESFaq(object):
    """ES构建FAQ召回"""

    def __init__(self, ip, port):
        """连接es数据库"""
        self.es = Elasticsearch(hosts=[{"host": ip, "port": port}], timeout=10000)  # [], 连接集群，以列表的形式存放各节点的IP地址

    def creat_index(self, index_name):
        """创建索引, 同时设置mappings"""
        mappings = {"mappings": {
            "properties": {
                "id": {
                    "type": "long",
                    "index": "true"
                },
                "question": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "answer": {
                    "type": "text",
                    "analyzer": "ik_smart"
                }
            }
        }}
        self.es.indices.create(index=index_name, body=mappings)

    def delete_index(self, index_name):
        """删除索引"""
        self.es.indices.delete(index_name)

    def insert_one(self, index_name, data=None):
        """单条导入"""
        data = {
            "id": 0,
            "question": "提前还款需要手续费吗",
            "answer": "传统金融机构大多要求用户在还款日当天还款，用户如果希望提前还款，需要申请并缴纳手续费。除常规默认代扣还款外，“微粒贷”亦支持用户随时结清贷款，且不收取任何其他额外手续费用。。"
        }
        self.es.index(index=index_name, body=data)

    def insert_batch(self, index_name, file_in):
        """批量导入"""
        st = time.time()
        datas = get_datas(file_in)
        bulk(client=self.es, actions=datas, index=index_name)
        print("耗时： {}， 插入条数： {}".format(time.time() - st, len(datas)))

    def delete(self, index_name):
        """删除数据"""
        # 根据字段删除, id字段
        delete_by_id = {"query": {"match": {"id": 10000}}}
        # 删除全部
        delete_by_all = {"query": {"match_all": {}}}
        result = self.es.delete_by_query(index=index_name, body=delete_by_id)
        print(result)

    def update(self, index_name):
        """更新数据"""
        id = ""
        body = {"doc": {"is_linked": 0}}
        self.es.update(index=index_name, id=id, body=body)

    def search(self, index_name, query):
        """检索召回"""
        body = {"query": {"match": {"question": query}}}
        result = self.es.search(index=index_name, size=10, body=body)
        recall = get_result(result)
        return recall


if __name__ == '__main__':
    esfaq = ESFaq(ip='0.0.0.0', port=9200)
    # esfaq.creat_index('weilidai')
    # esfaq.insert_one()
    # esfaq.insert_batch('微粒贷', 'data/weilidai.txt')
    while 1:
        query = input(">>>: ")
        st = time.time()
        result = esfaq.search('微粒贷', query)
        print(result)
        print(time.time() - st)
