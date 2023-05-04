import csv
import random
import networkx as nx
import pandas as pd
import pymongo
import matplotlib.pyplot as plt
import heapq
import numpy as np


def get_data_from_txt(filename):
    data = pd.read_csv(filename, names=['col1', 'col2'], header=None, sep=' ')
    data_cut = data.head(100)
    return data_cut


def build_net_from_mongodb():
    for x in col.find({}, {"_id": 0, "源微博用户id": 1, "评论或转发或点赞用户id": 1}).limit(100):
        edge_weight = random.random()
        g.add_edge(x["源微博用户id"], x["评论或转发或点赞用户id"])
    for node in g:
        g.add_node(node, state=0, theta=1)
    nx.draw_networkx(g, node_size=5, width=0.1, with_labels=False)
    plt.show()


# 读入数据并初始化（weight随机选取，初始标识都为0）
def build_net_from_txt():
    data = get_data_from_txt(filepath)
    for i in data.index:
        # 边传播概率：0-1之间的随机数
        edge_weight = random.random()
        g.add_edge(data.loc[i][0], data.loc[i][1], weight=edge_weight)
    # state: 节点分为激活与未激活两种状态，0表示未激活，1表示激活    theta: 传播阈值
    for node in g:
        g.add_node(node, state=0, theta=1)
    # print(len(list(g.nodes)))
    nx.draw_networkx(g, node_size=5, width=0.1, with_labels=False)
    plt.show()


# 选择度最大的n个节点
def select_active_node(n):
    print(nx.degree(g))
    # keys = list(node_degree_dic.keys())
    # values = list(node_degree_dic.values())
    # index_list = []
    # author_list = []
    # degree_list = []
    # # print(keys)
    # max_number = heapq.nlargest(n, values)
    # for value in max_number:
    #     index_list.append(values.index(value))
    # for i in range(len(index_list)):
    #     author_list.append(keys[index_list[i]])
    #     degree_list.append(values[index_list[i]])
    # # print(index_list)
    # # print(author_list)
    # # print(degree_list)
    # return author_list


# def spread(g):
#     sum_a = []
#     now_a = []
#     now_a_nbr_dic = {}
#     now_a_nbr_list = []
#
#     sum_b = []
#     now_b = []
#     now_b_nbr_dic = {}
#     now_b_nbr_list = []
#
#     same_node = []
#
#     for node in a_list:
#         g.nodes[node]['state'] = 1
#         sum_a.append(node)
#         now_a.append(node)
#     for node in b_list:
#         g.nodes[node]['state'] = 2
#         sum_b.append(node)
#         now_b.append(node)
#
#     for i in range(iter_num):
#         for a in now_a:
#             nbr_list = []
#             for nbr in g.neighbors(a):
#                 nbr_list.append(nbr)
#                 now_a_nbr_list.append(nbr)
#             now_a_nbr_dic[a] = nbr_list
#             now_a_nbr_list = list(set(now_a_nbr_list))
#
#         for b in now_b:
#             nbr_list = []
#             for nbr in g.neighbors(b):
#                 nbr_list.append(nbr)
#                 now_b_nbr_list.append(nbr)
#             now_b_nbr_dic[b] = nbr_list
#             now_b_nbr_list = list(set(now_b_nbr_list))
#
#         same_node = set(now_a_nbr_list) & set(now_b_nbr_list)
#
#         now_a = []
#         now_b = []
#
#         # a信息节点传播
#         for a in now_a_nbr_dic:
#             for nbr in now_a_nbr_dic[a]:
#                 if g.nodes[nbr]['state'] == 0:
#                     if nbr not in same_node:
#                         if random.random() < g[a][nbr]['weight'] and g.nodes[a]['theta'] * g[a][nbr]['weight'] >= theta:
#                             g.nodes[nbr]['state'] = 1
#                             g.nodes[nbr]['theta'] = g.nodes[a]['theta'] * g[a][nbr]['weight']
#                             now_a.append(nbr)
#                             sum_a.append(nbr)
#                     else:
#                         if random.random() < g[a][nbr]['weight']:
#                             g.nodes[nbr]['a_theta'] = g.nodes[a]['theta'] * g[a][nbr]['weight']
#                             g.nodes[nbr]['a_state'] = 1
#
#         # b信息节点传播
#         for b in now_a_nbr_dic:
#             for nbr in now_a_nbr_dic[b]:
#                 if g.nodes[nbr]['state'] == 0:
#                     if nbr not in same_node:
#                         if random.random() < g[b][nbr]['weight'] and g.nodes[b]['theta'] * g[b][nbr]['weight'] >= theta:
#                             g.nodes[nbr]['state'] = 2
#                             g.nodes[nbr]['theta'] = g.nodes[b]['theta'] * g[b][nbr]['weight']
#                             now_b.append(nbr)
#                             sum_b.append(nbr)
#                     else:
#                         if random.random() < g[b][nbr]['weight']:
#                             g.nodes[nbr]['b_theta'] = g.nodes[b]['theta'] * g[b][nbr]['weight']
#                             g.nodes[nbr]['b_state'] = 1
#
#         # 共同影响处理
#         for node in same_node:
#             if g.nodes[node]['a_state'] == 1 and g.nodes[node]['b_state'] == 1:
#                 if random.random() > 0.5:
#                     g.nodes[node]['state'] = 1
#                     g.nodes[node]['theta'] = g.nodes[node]['a_theta']
#                     now_a.append(node)
#                     sum_a.append(node)
#                 else:
#                     g.nodes[node]['state'] = 2
#                     g.nodes[node]['theta'] = g.nodes[node]['b_theta']
#                     now_b.append(node)
#                     sum_b.append(node)
#             elif g.nodes[node]['a_state'] == 1 and g.nodes[node]['b_state'] == 0:
#                 g.nodes[node]['state'] = 1
#                 g.nodes[node]['theta'] = g.nodes[node]['a_theta']
#                 now_a.append(node)
#                 sum_a.append(node)
#             elif g.nodes[node]['a_state'] == 0 and g.nodes[node]['b_state'] == 1:
#                 g.nodes[node]['state'] = 2
#                 g.nodes[node]['theta'] = g.nodes[node]['b_theta']
#                 now_b.append(node)
#                 sum_b.append(node)
#             else:
#                 g.nodes[node]['state'] = 0
#         print('第', i, '轮激活的a：', now_a)
#         print('第', i, '轮激活的b：', now_b)
#
#         now_a_nbr_dic = {}
#         now_a_nbr_list = []
#         now_b_nbr_dic = {}
#         now_b_nbr_list = []
#         same_node = []
#
#     print('最终激活的a：', sum_a)
#     print('最终激活的b：', sum_b)
#
#     return 1


if __name__ == '__main__':
    g = nx.Graph()

    filepath = r"D:\Study\data\graphData\facebook\facebook_combined.txt"

    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client["war"]  # db = client["war"] col = db["person"] ; db = client["war"] col = db[# "content"]
    col = db["content"]

    # input:  the path of the txt file which contains the graph data
    # output:  the list of edges
    # build_net_from_txt()
    # 获取每个节点的度列表 g.degree(node)
    # select_active_node(3)

    build_net_from_mongodb()
