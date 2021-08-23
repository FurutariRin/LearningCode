import datetime
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import re
import jsonpath
import requests
import csv
import time
import sys
import pandas as pd
import tqdm

url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
head = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
}
statisticsData = re.compile(r'"statisticsData":"(.*?)"')
provinceName = re.compile(r'"provinceName":"(.*?)"')


class JsonData:
    def __init__(self, province, jsonURL):
        self.province = province
        self.jsonURL = jsonURL

    def println(self):
        for i in (self.province + self.jsonURL):
            print(i)


class EpidemicData:
    def __init__(self, confirmedCount, confirmedIncr, curedCount, curedIncr,
                 currentConfirmedCount, currentConfirmedIncr, dateId,
                 deadCount, deadIncr, highDangerCount, midDangerCount,
                 suspectedCount, suspectedCountIncr):
        self.confirmedCount = confirmedCount  #确诊总数
        self.confirmedIncr = confirmedIncr  #今日确诊数
        self.curedCount = curedCount  #治愈总数
        self.curedIncr = curedIncr  #治愈新增
        self.currentConfirmedCount = currentConfirmedCount  #现存感染数
        self.currentConfirmedIncr = currentConfirmedIncr  #现存增加数
        self.dateId = dateId  #日期
        self.deadCount = deadCount  #死亡人数
        self.deadIncr = deadIncr  #新增死亡
        self.highDangerCount = highDangerCount  #高风险地区数
        self.midDangerCount = midDangerCount  #中风险地区数
        self.suspectedCount = suspectedCount  #疑似总数
        self.suspectedCountIncr = suspectedCountIncr  #新增疑似


def getJSON(url):  #获取JSONURL
    dataList = ""
    req = urllib.request.Request(url, headers=head)
    res = urllib.request.urlopen(req)
    html = res.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    for i in soup.find_all(id="getAreaStat"):
        i = str(i)
        province = re.findall(provinceName, i)
        link = re.findall(statisticsData, i)
        data = JsonData(province, link)
        dataList = data
    return dataList


def getData(url):
    data = []
    res = requests.get(url).json()
    dateId = jsonpath.jsonpath(res, "$..dateId")
    confirmedCount = jsonpath.jsonpath(res, "$..confirmedCount")
    confirmedIncr = jsonpath.jsonpath(res, "$..confirmedIncr")
    curedCount = jsonpath.jsonpath(res, "$..curedCount")
    curedIncr = jsonpath.jsonpath(res, "$..curedIncr")
    currentConfirmedCount = jsonpath.jsonpath(res, "$..currentConfirmedCount")
    currentConfirmedIncr = jsonpath.jsonpath(res, "$..currentConfirmedIncr")
    deadCount = jsonpath.jsonpath(res, "$..deadCount")
    deadIncr = jsonpath.jsonpath(res, "$..deadIncr")
    highDangerCount = jsonpath.jsonpath(res, "$..highDangerCount")
    midDangerCount = jsonpath.jsonpath(res, "$..midDangerCount")
    suspectedCount = jsonpath.jsonpath(res, "$..suspectedCount")
    suspectedCountIncr = jsonpath.jsonpath(res, "$..suspectedCountIncr")
    epidemicData = EpidemicData(confirmedCount, confirmedIncr, curedCount,
                                curedIncr, currentConfirmedCount,
                                currentConfirmedIncr, dateId, deadCount,
                                deadIncr, highDangerCount, midDangerCount,
                                suspectedCount, suspectedCountIncr)
    data.append(epidemicData)
    return data


jsonData = getJSON(url)
# data.println()
# print(data.province[0])
# print(jsonData.jsonURL[6])
data = []
for i in tqdm.tqdm(range(0, len(jsonData.jsonURL)),
                   desc="处理JSON文件",
                   unit="个文件"):
    # print(jsonData.jsonURL[i])
    data.append(getData(jsonData.jsonURL[i]))
    # print("\r", end="")
    # print("Download progress: {}%: {}/{}".format(
    #     int(float(i / (len(jsonData.jsonURL) - 1)) * 100), i + 1,
    #     len(jsonData.jsonURL)),
    #       "▋" * int(float(i / len(jsonData.jsonURL)) * 50),
    #       end="")
    # sys.stdout.flush()
AllData = []
# print(len(data))
i = 0
while i < len(data):
    Data = dict(area=jsonData.province[i], Data=data[i])
    AllData.append(Data)
    i = i + 1
print("\n我爬完了")
# print(AllData[0]["Data"][0].dateId[0])
# print(len(AllData[0]["Data"][0].dateId))
n = 0
while n < len(AllData):
    fileName = "爬虫数据\\初始数据\\" + str(n) + ".csv"
    # print(str(n)+","+AllData[n]["area"])
    f = open(fileName, "w", encoding="utf-8", newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow([
        "日期", "确诊总数", "今日确诊数", "治愈总数", "治愈新增", "现存感染数", "现存增加数", "死亡人数",
        "新增死亡", "高风险地区数", "中风险地区数", "疑似总数", "新增疑似"
    ])
    m = 0
    while m < len(AllData[n]["Data"][0].dateId):
        csv_writer.writerow([
            AllData[n]["Data"][0].dateId[m],
            AllData[n]["Data"][0].confirmedCount[m],
            AllData[n]["Data"][0].confirmedIncr[m],
            AllData[n]["Data"][0].curedCount[m],
            AllData[n]["Data"][0].curedIncr[m],
            AllData[n]["Data"][0].currentConfirmedCount[m],
            AllData[n]["Data"][0].currentConfirmedIncr[m],
            AllData[n]["Data"][0].deadCount[m],
            AllData[n]["Data"][0].deadIncr[m],
            AllData[n]["Data"][0].highDangerCount[m],
            AllData[n]["Data"][0].midDangerCount[m],
            AllData[n]["Data"][0].suspectedCount[m],
            AllData[n]["Data"][0].suspectedCountIncr[m]
        ])
        m = m + 1
    f.close()
    n = n + 1
# MinDate = datetime.date(1970, 1, 1)
# for i in range(len(AllData)):
#     time_tuple = time.strptime(str(AllData[i]["Data"][0].dateId[0]), "%Y%m%d")
#     year, month, day = time_tuple[:3]
#     getDate = datetime.date(year, month, day)
#     if (getDate > MinDate):
#         MinDate = getDate
# print(MinDate)
# for i in range(len(AllData)):
#     pretreatmentData = []
#     UseDate = MinDate
#     for n in range(len(AllData[i]["Data"][0].dateId)):
#         time_tuple = time.strptime(str(AllData[i]["Data"][0].dateId[n]),
#                                    "%Y%m%d")
#         year, month, day = time_tuple[:3]
#         getDate = datetime.date(year, month, day)
#         if (getDate == UseDate):
#             epidemicData = EpidemicData(
#                 AllData[i]["Data"][0].confirmedCount[n],
#                 AllData[i]["Data"][0].confirmedIncr[n],
#                 AllData[i]["Data"][0].curedCount[n],
#                 AllData[i]["Data"][0].curedIncr[n],
#                 AllData[i]["Data"][0].currentConfirmedCount[n],
#                 AllData[i]["Data"][0].currentConfirmedIncr[n],
#                 AllData[i]["Data"][0].dateId[n],
#                 AllData[i]["Data"][0].deadCount[n],
#                 AllData[i]["Data"][0].deadIncr[n],
#                 AllData[i]["Data"][0].highDangerCount[n],
#                 AllData[i]["Data"][0].midDangerCount[n],
#                 AllData[i]["Data"][0].suspectedCount[n],
#                 AllData[i]["Data"][0].suspectedCountIncr[n])
#             pretreatmentData.append(epidemicData)
#             UseDate = UseDate + datetime.timedelta(days=1)
#     fileName = "爬虫数据\\预处理数据\\" + str(n) + ".csv"
#     f = open(fileName, "w", encoding="utf-8", newline="")
#     csv_writer = csv.writer(f)
#     csv_writer.writerow([
#         "日期", "确诊总数", "今日确诊数", "治愈总数", "治愈新增", "现存感染数", "现存增加数", "死亡人数",
#         "新增死亡", "高风险地区数", "中风险地区数", "疑似总数", "新增疑似"
#     ])
#     for x in len(AllData[n]["Data"][0].dateId):
#         # haha=AllData[n]["Data"][0].dateId[m]
#         csv_writer.writerow([
#             AllData[n]["Data"][0].dateId[x],
#             AllData[n]["Data"][0].confirmedCount[x],
#             AllData[n]["Data"][0].confirmedIncr[x],
#             AllData[n]["Data"][0].curedCount[x],
#             AllData[n]["Data"][0].curedIncr[x],
#             AllData[n]["Data"][0].currentConfirmedCount[x],
#             AllData[n]["Data"][0].currentConfirmedIncr[x],
#             AllData[n]["Data"][0].deadCount[x],
#             AllData[n]["Data"][0].deadIncr[x],
#             AllData[n]["Data"][0].highDangerCount[x],
#             AllData[n]["Data"][0].midDangerCount[x],
#             AllData[n]["Data"][0].suspectedCount[x],
#             AllData[n]["Data"][0].suspectedCountIncr[x],
#         ])
#     f.close()
