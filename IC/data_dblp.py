# -*- coding:utf-8 -*-
import sys
from xml.sax import handler, make_parser
import pickle
import os
import csv

DBLP_XML_PATH = r'E:\dataset\DBLP\dblp.xml'
# 此处需要完整添加所有“块”结构的标签，或者需要处理的类型的标签
paperTag = ('article', 'inproceedings', 'proceedings', 'book',
            'incollection', 'phdthesis', 'mastersthesis', 'www')


class CoauthorHandler(handler.ContentHandler):
    def __init__(self):
        self.title = ''
        self.year = ''
        self.author = ''
        self.journal = ''

        self.count = 0
        self.count2 = 0

        self.isPaperTag = 0
        self.isTitleTag = 0
        self.isYearTag = 0
        self.isAuthorTag = 0
        self.isJournalTag = 0

        # self.authors = ''
        self.authors = []  # 存储每个“块”中的所有author
        self.storage = {}  # 用来存储生成的数据，结构为{'title':[year, [author1, author2, ...]]}
        # with open(file_path, "wb") as csvfile:

    def startDocument(self):
        print('Document Start')

    def endDocument(self):
        print('Document End')

    def startElement(self, name, attrs):
        if name in paperTag:
            self.isPaperTag = 1
        if name == 'title':
            self.isTitleTag = 1
        if name == 'author':
            self.isAuthorTag = 1
        if name == 'year':
            self.isYearTag = 1
        if name == 'journal':
            self.isJournalTag = 1

    def endElement(self, name):
        if name == 'author':
            self.authors.append(self.author)
            # self.authors=self.authors+self.author
            # print(self.author)
            # print(self.authors)
            self.author = ''
            self.count2 += 1
            # del self.authors
            # self.authors = []
        if name == 'year' or name == 'title':
            pass
        if name in paperTag:
            if self.count2 > 1:  # 删除单个作者的文献
                self.count += 1
                self.storage[self.title] = []
                self.storage[self.title].append(self.year)
                self.storage[self.title].append(self.authors)
                self.storage[self.title].append(self.journal)
                self.year = ''
                self.authors = []
                self.journal = ''
                self.count2 = 0
                # if self.count % 1 == 0:
                if self.count % 1000 == 0:  # 每1000轮输出一次提示信息
                    print(self.count)
                    # print(self.author)
                    # print('\n')
                    # exit(0)
                    # if count == 468:
                    # str=input('请输入零')
                    # items = self.storage.items()
                    # with open("D:\dblp.csv",'a',newline='',encoding='utf-8') as csvfile:#a
                    # writer = csv.writer(csvfile)#,dialect='excel'
                    # if count == 468:
                    # str=input('请输入一')
                    # for item in items:
                    # tmp_li = []
                    # tmp_li.append(item[0])
                    # tmp_li.append(item[1][0])
                    # tmp_li.append(item[1][1])
                    # writer.writerow(tmp_li)
                    # if count == 468:
                    # str=input('请输入六')
                    # saveToCsv(self.storage,"D:\\dblp.csv")
                    # print(self.storage)
                    # self.storage = {}
                    # self.storage = {}

                    if self.count % 1000 == 0:
                        # if self.count % 10 == 0:
                        print('已保存')
                        saveToCsv(self.storage, r'D:\study\Pyfiles\bysj\dblp_1000.csv')

                        exit(0)
                        # return

    def characters(self, content):
        if self.isTitleTag == 1:
            self.isTitleTag = 0
            self.title = content
        if self.isAuthorTag == 1:
            self.isAuthorTag = 0
            self.author = content
        if self.isYearTag == 1:
            self.isYearTag = 0
            self.year = content
        if self.isJournalTag == 1:
            self.isJournalTag = 0
            self.journal = content


def parserDblpXml():
    handler = CoauthorHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    f = open(DBLP_XML_PATH, 'r')
    parser.parse(f)
    f.close()
    return handler.storage


def saveToCsv(storage, file_path):
    items = storage.items()
    # with open(file_path, "wb") as csvfile:
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:  # a
        writer = csv.writer(csvfile)  # ,dialect='excel'
        for item in items:
            tmp_li = [item[0], item[1][0], item[1][1], item[1][2]]
            writer.writerow(tmp_li)
        csvfile.close()


if __name__ == '__main__':
    storage = parserDblpXml()
