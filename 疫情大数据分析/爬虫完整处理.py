"""
该文件包括了自动生成初始数据，预处理数据，中国数据，省份最新数据的功能
"""
from tqdm import tqdm
import pandas as pd
import time
import datetime
import json
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import re
import requests
import csv
import tqdm

url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
head = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
}
statisticsData = re.compile(r'"statisticsData":"(.*?)"')
provinceName = re.compile(r'"provinceShortName":"(.*?)"')


def getJSON(url):  # 获取JSONURL
    req = urllib.request.Request(url, headers=head)
    res = urllib.request.urlopen(req)
    html = res.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    for i in soup.find_all(id="getAreaStat"):
        i = str(i)
        province = re.findall(provinceName, i)
        link = re.findall(statisticsData, i)
        data = {"省份": province, "Json": link}
    FinalData = []
    for i in range(len(province)):
        FinalData.append({"省份": data["省份"][i], "Json": data["Json"][i]})
    return FinalData


jsonData = getJSON(url)
data = []
for i in tqdm.tqdm(range(len(jsonData)), desc="处理JSON文件", unit="files"):
    res = requests.get(jsonData[i]["Json"]).json()
    data.append({"Province": jsonData[i]["省份"], "Data": res["data"]})
print("\n我爬完了")
filePath = "疫情大数据分析\\爬虫数据\\初始数据\\初始数据.json"
f = open(filePath, "w", encoding="utf-8", newline="")
json.dump(data, f, ensure_ascii=False)
# print(data[9]["Data"][565])
for i in range(len(data)):
    fileName = "疫情大数据分析\\爬虫数据\\初始数据\\" + str(i) + ".csv"
    f = open(fileName, "w", encoding="utf-8", newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow([
        "日期", "确诊总数", "今日确诊数", "治愈总数", "治愈新增", "现存感染数", "现存增加数", "死亡人数",
        "新增死亡", "高风险地区数", "中风险地区数", "疑似总数", "新增疑似"
    ])
    for n in range(len(data[i]["Data"])):
        csv_writer.writerow([data[i]["Data"][n]["dateId"],
                             data[i]["Data"][n]["confirmedCount"],
                             data[i]["Data"][n]["confirmedIncr"],
                             data[i]["Data"][n]["curedCount"],
                             data[i]["Data"][n]["curedIncr"],
                             data[i]["Data"][n]["currentConfirmedCount"],
                             data[i]["Data"][n]["currentConfirmedIncr"],
                             data[i]["Data"][n]["deadCount"],
                             data[i]["Data"][n]["deadIncr"],
                             data[i]["Data"][n]["highDangerCount"],
                             data[i]["Data"][n]["midDangerCount"],
                             data[i]["Data"][n]["suspectedCount"],
                             data[i]["Data"][n]["suspectedCountIncr"]])
    f.close()


i = 0
for i in range(0, 34):
    fileName = "疫情大数据分析\\爬虫数据\\初始数据\\" + str(i) + ".csv"
    data = pd.read_csv(fileName, encoding="utf-8")
    MinDate = datetime.date(1970, 1, 1)
    time_tuple = time.strptime(str(data["日期"][data["日期"].argmin()]), "%Y%m%d")
    year, month, day = time_tuple[:3]
    getDate = datetime.date(year, month, day)
    if (getDate > MinDate):
        MinDate = getDate

i = 0
for i in tqdm.tqdm(range(0, 34), unit="个省", desc="处理省份疫情数据"):
    fileName = "疫情大数据分析\\爬虫数据\\初始数据\\" + str(i) + ".csv"
    data = pd.read_csv(fileName, encoding="utf-8")
    UseDate = MinDate
    fileName = "疫情大数据分析\\爬虫数据\\预处理数据\\" + str(i) + ".csv"
    f = open(fileName, "w", encoding="utf-8", newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow([
        "日期", "确诊总数", "今日确诊数", "治愈总数", "治愈新增", "现存感染数", "现存增加数", "死亡人数",
        "新增死亡", "高风险地区数", "中风险地区数", "疑似总数", "新增疑似"
    ])
    row = 0
    for row in range(len(data)):
        time_tuple = time.strptime(str(data.iloc[row]["日期"]), "%Y%m%d")
        year, month, day = time_tuple[:3]
        getDate = datetime.date(year, month, day)
        if (getDate >= MinDate):
            if (getDate != UseDate):
                csv_writer.writerow([
                    datetime.date.strftime(UseDate, "%Y%m%d"),
                    data.iloc[row - 1]["确诊总数"], data.iloc[row - 1]["今日确诊数"],
                    data.iloc[row - 1]["治愈总数"], data.iloc[row - 1]["治愈新增"],
                    data.iloc[row - 1]["现存感染数"], data.iloc[row - 1]["现存增加数"],
                    data.iloc[row - 1]["死亡人数"], data.iloc[row - 1]["新增死亡"],
                    data.iloc[row - 1]["高风险地区数"], data.iloc[row - 1]["中风险地区数"],
                    data.iloc[row - 1]["疑似总数"], data.iloc[row - 1]["新增疑似"]
                ])
                csv_writer.writerow([
                    data.iloc[row]["日期"], data.iloc[row]["确诊总数"],
                    data.iloc[row]["今日确诊数"], data.iloc[row]["治愈总数"],
                    data.iloc[row]["治愈新增"], data.iloc[row]["现存感染数"],
                    data.iloc[row]["现存增加数"], data.iloc[row]["死亡人数"],
                    data.iloc[row]["新增死亡"], data.iloc[row]["高风险地区数"],
                    data.iloc[row]["中风险地区数"], data.iloc[row]["疑似总数"],
                    data.iloc[row]["新增疑似"]
                ])
                UseDate = UseDate + datetime.timedelta(days=1)
            else:
                haha = data.iloc[row]["确诊总数"]
                csv_writer.writerow([
                    data.iloc[row]["日期"], data.iloc[row]["确诊总数"],
                    data.iloc[row]["今日确诊数"], data.iloc[row]["治愈总数"],
                    data.iloc[row]["治愈新增"], data.iloc[row]["现存感染数"],
                    data.iloc[row]["现存增加数"], data.iloc[row]["死亡人数"],
                    data.iloc[row]["新增死亡"], data.iloc[row]["高风险地区数"],
                    data.iloc[row]["中风险地区数"], data.iloc[row]["疑似总数"],
                    data.iloc[row]["新增疑似"]
                ])
            UseDate = UseDate + datetime.timedelta(days=1)
    if (str(data.iloc[len(data) - 1]["日期"]) !=
        (datetime.date.today() -
         datetime.timedelta(days=1)).strftime("%Y%m%d")):
        csv_writer.writerow([
            (datetime.date.today() -
             datetime.timedelta(days=1)).strftime("%Y%m%d"),
            data.iloc[len(data) - 1]["确诊总数"],
            data.iloc[len(data) - 1]["今日确诊数"],
            data.iloc[len(data) - 1]["治愈总数"], data.iloc[len(data) - 1]["治愈新增"],
            data.iloc[len(data) - 1]["现存感染数"],
            data.iloc[len(data) - 1]["现存增加数"],
            data.iloc[len(data) - 1]["死亡人数"], data.iloc[len(data) - 1]["新增死亡"],
            data.iloc[len(data) - 1]["高风险地区数"],
            data.iloc[len(data) - 1]["中风险地区数"],
            data.iloc[len(data) - 1]["疑似总数"], data.iloc[len(data) - 1]["新增疑似"]
        ])
    f.close()


fileName = "疫情大数据分析\\爬虫数据\\全国数据.csv"
f = open(fileName, "w", encoding="utf-8", newline="")
csv_writer = csv.writer(f)
csv_writer.writerow([
    "日期", "确诊总数", "今日确诊数", "治愈总数", "治愈新增", "现存感染数", "现存增加数", "死亡人数", "新增死亡",
    "高风险地区数", "中风险地区数", "疑似总数", "新增疑似"
])
UseData = pd.read_csv("疫情大数据分析\\爬虫数据\\预处理数据\\0.csv")
i = 0
for i in tqdm(range(len(UseData)), desc="统计全国每日数据", unit="Day"):
    dateId = UseData.iloc[i]["日期"]
    confirmedCount = 0
    confirmedIncr = 0
    curedCount = 0
    curedIncr = 0
    currentConfirmedCount = 0
    currentConfirmedIncr = 0
    deadCount = 0
    deadIncr = 0
    highDangerCount = 0
    midDangerCount = 0
    suspectedCount = 0
    suspectedCountIncr = 0
    x = 0
    for x in range(0, 34):
        filePath = "疫情大数据分析\\爬虫数据\\预处理数据\\" + str(x) + ".csv"
        data = pd.read_csv(filePath, encoding="utf-8")
        confirmedCount = confirmedCount + data.iloc[i]["确诊总数"]
        confirmedIncr = confirmedIncr + data.iloc[i]["今日确诊数"]
        curedCount = curedCount + data.iloc[i]["治愈总数"]
        curedIncr = curedIncr + data.iloc[i]["治愈新增"]
        currentConfirmedCount = currentConfirmedCount + data.iloc[i]["现存感染数"]
        currentConfirmedIncr = currentConfirmedIncr + data.iloc[i]["现存增加数"]
        deadCount = deadCount + data.iloc[i]["死亡人数"]
        deadIncr = deadIncr + data.iloc[i]["新增死亡"]
        highDangerCount = highDangerCount + data.iloc[i]["高风险地区数"]
        midDangerCount = midDangerCount + data.iloc[i]["中风险地区数"]
        suspectedCount = suspectedCount + data.iloc[i]["疑似总数"]
        suspectedCountIncr = suspectedCountIncr + data.iloc[i]["新增疑似"]
    csv_writer.writerow([
        dateId, confirmedCount, confirmedIncr, curedCount, curedIncr,
        currentConfirmedCount, currentConfirmedIncr, deadCount, deadIncr,
        highDangerCount, midDangerCount, suspectedCount, suspectedCountIncr
    ])
f.close()


fileName = "疫情大数据分析\\爬虫数据\\省份最新数据统计.csv"
f = open(fileName, "w", encoding="utf-8", newline="")
csv_writer = csv.writer(f)
csv_writer.writerow([
    "日期", "省份", "确诊总数", "今日确诊数", "治愈总数", "治愈新增", "现存感染数", "现存增加数", "死亡人数",
    "新增死亡", "高风险地区数", "中风险地区数", "疑似总数", "新增疑似"
])
i = 0
for i in tqdm(range(0, 34), desc="写入省份最新数据", unit="个省"):
    filePath = "疫情大数据分析\\爬虫数据\\预处理数据\\" + str(i) + ".csv"
    data = pd.read_csv(filePath, encoding="utf-8")
    area = pd.read_csv("疫情大数据分析\\爬虫数据\\代号意义.csv", encoding="utf-8")
    MaxDate = str(data["日期"][data["日期"].argmax()])
    ibasho = area["意义"][i]
    confirmedCount = data.iloc[data["日期"].argmax()]["确诊总数"]
    confirmedIncr = data.iloc[data["日期"].argmax()]["今日确诊数"]
    curedCount = data.iloc[data["日期"].argmax()]["治愈总数"]
    curedIncr = data.iloc[data["日期"].argmax()]["治愈新增"]
    currentConfirmedCount = data.iloc[data["日期"].argmax()]["现存感染数"]
    currentConfirmedIncr = data.iloc[data["日期"].argmax()]["现存增加数"]
    deadCount = data.iloc[data["日期"].argmax()]["死亡人数"]
    deadIncr = data.iloc[data["日期"].argmax()]["新增死亡"]
    highDangerCount = data.iloc[data["日期"].argmax()]["高风险地区数"]
    midDangerCount = data.iloc[data["日期"].argmax()]["中风险地区数"]
    suspectedCount = data.iloc[data["日期"].argmax()]["疑似总数"]
    suspectedCountIncr = data.iloc[data["日期"].argmax()]["新增疑似"]
    csv_writer.writerow([
        MaxDate, ibasho, confirmedCount, confirmedIncr, curedCount, curedIncr,
        currentConfirmedCount, currentConfirmedIncr, deadCount, deadIncr,
        highDangerCount, midDangerCount, suspectedCount, suspectedCountIncr
    ])
f.close()


filePath = "疫情大数据分析\\爬虫数据\\全国死亡率与治愈率.csv"
f = open(filePath, "w", encoding="utf-8", newline="")
csv_writer = csv.writer(f)
csv_writer.writerow(["日期", "确诊总数", "治愈总数", "死亡人数",
                    "感染死亡率", "感染治愈率", "住院死亡率", "住院治愈率"])
UseData = pd.read_csv("疫情大数据分析\\爬虫数据\\全国数据.csv")
for i in tqdm(range(len(UseData)), desc="计算死亡率与治愈率", unit="Day"):
    Date = UseData.iloc[i]["日期"]
    confirmedCount = UseData.iloc[i]["确诊总数"]
    curedCount = UseData.iloc[i]["治愈总数"]
    deadCount = UseData.iloc[i]["死亡人数"]
    CDP = float(deadCount/confirmedCount)
    CCP = float(curedCount/confirmedCount)
    HDP = float(deadCount/(deadCount+curedCount))
    HCP = float(curedCount/(deadCount+curedCount))
    csv_writer.writerow([Date, confirmedCount, curedCount,
                        deadCount, CDP, CCP, HDP, HCP])
f.close()
