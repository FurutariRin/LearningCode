import pandas as pd
import csv
from tqdm import tqdm

fileName = "疫情大数据分析\\爬虫数据\\全国数据.csv"
f = open(fileName, "w", encoding="utf-8", newline="")
csv_writer = csv.writer(f)
csv_writer.writerow([
    "日期", "确诊总数", "今日确诊数", "治愈总数", "治愈新增", "现存感染数", "现存增加数", "死亡人数", "新增死亡",
    "高风险地区数", "中风险地区数", "疑似总数", "新增疑似"
])
UseData = pd.read_csv("疫情大数据分析\\爬虫数据\\预处理数据\\0.csv")
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
