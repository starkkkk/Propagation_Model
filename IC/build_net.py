import csv
import random
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import heapq
import numpy as np


def get_data(filename):
    labels = ['title', 'year', 'author', 'journal']
    data = pd.read_csv(filename, names=labels)
    data_cut = data.head(1000)
    return data_cut


def get_target_authors(data, year):
    t_authors = []
    for i in range(len(data)):
        if data['year'][i] == year:
            t_author_list = eval(data['author'][i])
            for author in t_author_list:
                t_authors.append(author)
    t_authors = list(set(t_authors))
    # print('选择的目标节点：', t_authors)
    return t_authors


# 读入数据并初始化（weight随机选取，初始标识都为0）
def build_net(data):
    G = nx.Graph()
    # print(data)
    for paper in data:
        # print('paper')
        author_list = eval(paper)
        for author in author_list:
            if author != author_list[0]:
                # print([author, author_list[0]])
                edge_weight = random.choice(weight_list)
                G.add_edge(author, author_list[0], weight=edge_weight)
    for node in G:
        G.add_node(node, state=0)
        G.add_node(node, a_state=0)
        G.add_node(node, b_state=0)
        G.add_node(node, theta=1)
        G.add_node(node, a_theta=1)
        G.add_node(node, b_theta=1)

    # print(len(list(G.nodes)))
    nx.draw_networkx(G, node_size=5, width=0.1, with_labels=False)
    plt.show()
    # nx.write_gexf(G, 'net-Networkx.gexf')
    return G


#   获取每个节点的度列表
def get_degree(G):
    node_degree = {}
    for node in G.nodes:
        node_degree[node] = G.degree(node)
    return node_degree


#   选择度最大的n个节点激活
def select_active_node(n):
    keys = list(node_degree_dic.keys())
    values = list(node_degree_dic.values())
    index_list = []
    author_list = []
    degree_list = []
    # print(keys)
    max_number = heapq.nlargest(n, values)
    for value in max_number:
        index_list.append(values.index(value))
    for i in range(len(index_list)):
        author_list.append(keys[index_list[i]])
        degree_list.append(values[index_list[i]])
    # print(index_list)
    # print(author_list)
    # print(degree_list)
    return author_list


def spread(g):
    sum_a = []
    now_a = []
    now_a_nbr_dic = {}
    now_a_nbr_list = []

    sum_b = []
    now_b = []
    now_b_nbr_dic = {}
    now_b_nbr_list = []

    same_node = []

    for node in a_list:
        g.nodes[node]['state'] = 1
        sum_a.append(node)
        now_a.append(node)
    for node in b_list:
        g.nodes[node]['state'] = 2
        sum_b.append(node)
        now_b.append(node)

    for i in range(iter_num):
        for a in now_a:
            nbr_list = []
            for nbr in g.neighbors(a):
                nbr_list.append(nbr)
                now_a_nbr_list.append(nbr)
            now_a_nbr_dic[a] = nbr_list
            now_a_nbr_list = list(set(now_a_nbr_list))

        for b in now_b:
            nbr_list = []
            for nbr in g.neighbors(b):
                nbr_list.append(nbr)
                now_b_nbr_list.append(nbr)
            now_b_nbr_dic[b] = nbr_list
            now_b_nbr_list = list(set(now_b_nbr_list))

        same_node = set(now_a_nbr_list) & set(now_b_nbr_list)

        now_a = []
        now_b = []

        # a信息节点传播
        for a in now_a_nbr_dic:
            for nbr in now_a_nbr_dic[a]:
                if g.nodes[nbr]['state'] == 0:
                    if nbr not in same_node:
                        if random.random() < g[a][nbr]['weight'] and g.nodes[a]['theta'] * g[a][nbr]['weight'] >= theta:
                            g.nodes[nbr]['state'] = 1
                            g.nodes[nbr]['theta'] = g.nodes[a]['theta'] * g[a][nbr]['weight']
                            now_a.append(nbr)
                            sum_a.append(nbr)
                    else:
                        if random.random() < g[a][nbr]['weight']:
                            g.nodes[nbr]['a_theta'] = g.nodes[a]['theta'] * g[a][nbr]['weight']
                            g.nodes[nbr]['a_state'] = 1

        # b信息节点传播
        for b in now_a_nbr_dic:
            for nbr in now_a_nbr_dic[b]:
                if g.nodes[nbr]['state'] == 0:
                    if nbr not in same_node:
                        if random.random() < g[b][nbr]['weight'] and g.nodes[b]['theta'] * g[b][nbr]['weight'] >= theta:
                            g.nodes[nbr]['state'] = 2
                            g.nodes[nbr]['theta'] = g.nodes[b]['theta'] * g[b][nbr]['weight']
                            now_b.append(nbr)
                            sum_b.append(nbr)
                    else:
                        if random.random() < g[b][nbr]['weight']:
                            g.nodes[nbr]['b_theta'] = g.nodes[b]['theta'] * g[b][nbr]['weight']
                            g.nodes[nbr]['b_state'] = 1

        # 共同影响处理
        for node in same_node:
            if g.nodes[node]['a_state'] == 1 and g.nodes[node]['b_state'] == 1:
                if random.random() > 0.5:
                    g.nodes[node]['state'] = 1
                    g.nodes[node]['theta'] = g.nodes[node]['a_theta']
                    now_a.append(node)
                    sum_a.append(node)
                else:
                    g.nodes[node]['state'] = 2
                    g.nodes[node]['theta'] = g.nodes[node]['b_theta']
                    now_b.append(node)
                    sum_b.append(node)
            elif g.nodes[node]['a_state'] == 1 and g.nodes[node]['b_state'] == 0:
                g.nodes[node]['state'] = 1
                g.nodes[node]['theta'] = g.nodes[node]['a_theta']
                now_a.append(node)
                sum_a.append(node)
            elif g.nodes[node]['a_state'] == 0 and g.nodes[node]['b_state'] == 1:
                g.nodes[node]['state'] = 2
                g.nodes[node]['theta'] = g.nodes[node]['b_theta']
                now_b.append(node)
                sum_b.append(node)
            else:
                g.nodes[node]['state'] = 0
        print('第', i, '轮激活的a：', now_a)
        print('第', i, '轮激活的b：', now_b)

        now_a_nbr_dic = {}
        now_a_nbr_list = []
        now_b_nbr_dic = {}
        now_b_nbr_list = []
        same_node = []

    print('最终激活的a：', sum_a)
    print('最终激活的b：', sum_b)

    return 1


if __name__ == '__main__':
    theta = 0.01  # 传播阈值
    weight_list = [0.1, 0.01]  # 边权重
    data_set = 'dblp_1000.csv'  # dataset选择
    iter_num = 4        # 迭代轮数
    nn = 0
    author_data = get_data(data_set)
    target_authors = get_target_authors(author_data, 1993)
    g = build_net(author_data['author'])
    # 获取字典形式的度列表
    node_degree_dic = get_degree(g)
    # print(node_degree_dic)
    # 选择度最大节点
    a_list = select_active_node(4)
    print('度最大的n个节点：', a_list)

    # 选择算法得出的种子集
    b_list = ['Friedemann Leibfritz', 'Lothar Breuer', 'Florian Jarre', 'Petra Scheffler', 'Ulrich Raber', 'Benjamin Hurwitz',
              'Anna Slobodov', 'Jordan Gergov', 'Michael L. Brodie', 'Christoph Meinel']
    spread(g)
    for t_node in target_authors:
        if g.nodes[t_node]['state'] == 2:
            nn += 1
    print(target_authors)
    print('最终影响权重：', nn / len(target_authors))
