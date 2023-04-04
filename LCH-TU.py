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


def list_all_less_num(l1, number):
    for num in l1:
        if num >= number:
            return False
    return True


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
        G.add_node(node, state=0, a_state=0, b_state=0, theta=1, a_theta=1, b_theta=1, target=0, in_out1=[], in_out2=[])

    for node in target_authors:
        G.nodes[node]['target'] = 1

    # print(len(list(G.nodes)))
    # nx.draw_networkx(G, node_size=5, width=0.1, with_labels=False)
    # plt.show()
    # nx.write_gexf(G, 'net-Networkx.gexf')
    return G


def dijkstra(g, node):

    # shortest_path = {}

    # for node in target_authors:
    path_list = []
    now_list = [node]
    now_distance = [1]

    n = 1

    while n < 10:
        now_nbr_num_list = []
        # print('第', n, '轮')
        # print('源节点：', now_list)
        now_nbr_list = []
        now_nbr_weight = []

        # 获得现在的总邻居列表、相应的距离、每个列表内节点的邻居数量
        for i in range(len(now_list)):
            now_nbr_num_list.append(0)
            for nbr in g.neighbors(now_list[i]):
                if nbr not in now_list:
                    now_nbr_num_list[i] += 1
                    now_nbr_list.append(nbr)
                    now_nbr_weight.append(g[now_list[i]][nbr]['weight'] * now_distance[i])

        if list_all_less_num(now_nbr_weight, theta):
            # print('传播概率：', now_nbr_weight)
            # print('无可选择节点')
            break
        # print('邻居列表以及距离：', now_nbr_list, now_nbr_weight)
        # print('节点邻居数量：', now_nbr_num_list)

        # 获得本轮该加入的节点
        max_number = heapq.nlargest(1, now_nbr_weight)[0]
        index = now_nbr_weight.index(max_number)
        in_nbr = now_nbr_list[index]
        # print('本轮加入节点：', in_nbr)

        # 得到该新加入的节点是从哪个原节点传播出去的
        sum = 0
        k = 0
        while sum < index + 1:
            sum += now_nbr_num_list[k]
            k += 1
        # print('选择的动作：', now_list[k - 1], '——>', in_nbr)

        # 加入path_list
        if not path_list:
            new_path = [now_list[k - 1], in_nbr]
        else:
            if k == 1:
                new_path = [now_list[k - 1], in_nbr]
            else:
                for path in path_list:
                    if path[-1] == now_list[k - 1]:
                        new_path = path.copy()
                        new_path.append(in_nbr)
                        break
        path_list.append(new_path)
        now_list.append(in_nbr)
        now_distance.append(now_nbr_weight[index])

        # print('最大可能值、索引、名称：', max_number, index, in_nbr)
        # print('选择后的节点以及距离：', now_list, now_distance)
        # print('最短路径：', path_list)
        n += 1

    # 有用的数据
    #     print([path_list, now_list, now_distance])
    shortest_path = [path_list, now_list, now_distance]
    # print('最短路径信息', shortest_path)
    return shortest_path


def compare(x, y):
    for i in x:
        for j in y:
            if i == j:
                return True
    return False

# def t(x, y):


# def algorithm():
#
#         for u in path[1]:
#             ap_dic[u] = 0
#             t_dic[u] = 1
#             if u not in target_authors:
#                 f_dic[u] += t_dic[u]*(1-ap_dic[u])


# def compute_ap(x):
#     path = dijkstra(g, x)
#     print(path)
#     for node1 in path[1]:
#         if node1 in s:
#             ap_dic[node1] = 1:


def have_in_node(path_list, s_node):
    for p_path in path_list:
        if s_node in p_path:
            a = p_path.index(s_node)
            if len(p_path) > a + 1:
                return True
    return False


def ap(u):
    # print(path)
    w = 1
    if u in s:
        return 1
    else:
        if not have_in_node(path[0], u):
            return 0
        else:
            for p in path[0]:
                if u in p:
                    a = p.index(u)
                    if len(p) > a + 1:
                        w = w * (1-ap(p[a + 1]) * g[u][p[a + 1]]['weight'])
            return 1-w


def t(u, x):
    w = 1
    if x == u:
        return 1
    else:
        for p in path[0]:
            # print(p)
            if x in p:
                a = p.index(x)
                if p[a - 1] in s:
                    return 0
                else:
                    for nn in g.neighbors(p[a - 1]):
                        if p[a-2]:
                            if nn != p[a] and nn != p[a-2]:
                                w = w * (1-ap_dic[nn] * g[nn][p[a - 1]]['weight'])
                        else:
                            if nn != p[a]:
                                w = w * (1 - ap_dic[nn] * g[nn][p[a - 1]]['weight'])
                    return t(u, p[a - 1]) * g[x][p[a - 1]]['weight'] * w




if __name__ == '__main__':
    theta = 0.01  # 传播阈值
    weight_list = [0.1, 0.01, 0.001]  # 边权重
    data_set = 'dblp_1000.csv'  # dataset选择
    iter_num = 2
    max_seed = 10       # 选取种子数量
    now_seed = 0
    seed = []

    author_data = get_data(data_set)
    target_authors = get_target_authors(author_data, 1993)
    g = build_net(author_data['author'])
    # algorithm()


    # 初始化 [path_list, now_list, now_distance]
    s = []
    ap_dic = {}
    t_dic = {}
    f_dic = {}


    for node in g:
        f_dic[node] = 0
        ap_dic[node] = 0

    for node in target_authors:
        path = dijkstra(g, node)
        for n in path[1]:
            ap_dic[n] = ap(n)
            t_dic[n] = t(node, n)
            f_dic[n] += (1 - ap_dic[n]) * t_dic[n]
            # print(t_dic[n])

    while now_seed < max_seed:
        fv_list = []  # 除目标节点以外的节点相应的f值列表
        fn_list = []  # 除目标节点以外的节点列表
        for node in g:
            if node not in target_authors and node not in s:
                fv_list.append(f_dic[node])
                fn_list.append(node)
        # print(len(fn_list))
        # print(len(list(set(fn_list))))
        max1 = heapq.nlargest(1, fv_list)[0]
        index1 = fv_list.index(max1)
        name1 = fn_list[index1]

        s.append(name1)      #加入s中

        for node in target_authors:
            path = dijkstra(g, node)
            if name1 in path[1]:
                for node1 in path[1]:
                    f_dic[node1] -= (1 - ap_dic[node1]) * t_dic[node1]

        for node in target_authors:
            path = dijkstra(g, node)
            for n in path[1]:
                if n not in s:
                    ap_dic[n] = ap(n)
                    t_dic[n] = t(node, n)
                    f_dic[n] += (1 - ap_dic[n]) * t_dic[n]

        now_seed += 1

    print(s)






    # 获取字典形式的度列表
