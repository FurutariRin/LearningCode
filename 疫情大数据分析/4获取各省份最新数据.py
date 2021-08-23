import pandas as pd
import csv
from tqdm import tqdm

fileName = "爬虫数据\\省份最新数据统计.csv"
f = open(fileName, "w", encoding="utf-8", newline="")
csv_writer = csv.writer(f)
csv_writer.writerow([
    "日期", "省份", "确诊总数", "今日确诊数", "治愈总数", "治愈新增", "现存感染数", "现存增加数", "死亡人数",
    "新增死亡", "高风险地区数", "中风险地区数", "疑似总数", "新增疑似"
])
for i in tqdm(range(0, 34), desc="写入省份最新数据", unit="个省"):
    filePath = "爬虫数据\\预处理数据\\" + str(i) + ".csv"
    data = pd.read_csv(filePath, encoding="utf-8")
    area = pd.read_csv("爬虫数据\\代号意义.csv", encoding="utf-8")
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
