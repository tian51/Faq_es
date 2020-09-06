# -*- encoding: utf-8 -*-
"""
@File    : data_process.py
@Time    : 2020/9/5
@Author  : tyz
@Email   : 1239233794@qq.com
@Software: PyCharm
@desc    :
"""

import json


def get_datas(file_in):
    """读取本地文档构建actions,方便批量导入"""
    lines = [line.strip() for line in open(file_in, 'r', encoding='utf8').readlines()]
    datas = []
    for i, line in enumerate(lines):
        id = i
        q, k, a = line.split('\t')
        datas.append({"id": id, "question": q, "answer": a})
    return datas


def get_result(result):
    """过滤返回的结果"""
    recall = []
    for hit in result["hits"]["hits"]:
        recall.append({
            "score": hit['_score'],
            "id": hit['_source']['id'],
            "question": hit['_source']['question'],
            "answer": hit['_source']['answer'],
        })
    return json.dumps(recall, ensure_ascii=False, indent=2)
