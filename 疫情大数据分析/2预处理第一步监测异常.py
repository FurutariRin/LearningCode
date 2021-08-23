import datetime
import time
import pandas as pd
import tqdm
import csv

for i in range(0, 34):
    fileName = "疫情大数据分析\\爬虫数据\\初始数据\\" + str(i) + ".csv"
    data = pd.read_csv(fileName, encoding="utf-8")
    MinDate = datetime.date(1970, 1, 1)
    time_tuple = time.strptime(str(data["日期"][data["日期"].argmin()]), "%Y%m%d")
    year, month, day = time_tuple[:3]
    getDate = datetime.date(year, month, day)
    if (getDate > MinDate):
        MinDate = getDate
print(MinDate)

# for m in tqdm.tqdm(range(100)):
for i in tqdm.tqdm(range(0, 34), unit="个省", desc="处理省份疫情数据"):
    fileName = "疫情大数据分析\\爬虫数据\\初始数据\\" + str(i) + ".csv"
    data = pd.read_csv(fileName, encoding="utf-8")
    # pretreatmentData = pd.DataFrame()
    UseDate = MinDate
    fileName = "疫情大数据分析\\爬虫数据\\预处理数据\\" + str(i) + ".csv"
    f = open(fileName, "w", encoding="utf-8", newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow([
        "日期", "确诊总数", "今日确诊数", "治愈总数", "治愈新增", "现存感染数", "现存增加数", "死亡人数",
        "新增死亡", "高风险地区数", "中风险地区数", "疑似总数", "新增疑似"
    ])
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
                # pretreatmentData = pretreatmentData.append(data.iloc[[row - 1]])
                # print(str(i) + " " + str(UseDate))
                # pretreatmentData.iloc[row]["日期"] = datetime.date.strftime(
                #     UseDate, "%Y%m%d")
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
                # pretreatmentData = pretreatmentData.append(data.iloc[[row]])
                # pretreatmentData.append(
                #     pd.DataFrame({
                #         "日期": [data.iloc[row]["日期"]],
                #         "确诊总数": [data.iloc[row]["确诊总数"]],
                #         "今日确诊数": [data.iloc[row]["今日确诊数"]],
                #         "治愈总数": [data.iloc[row]["治愈总数"]],
                #         "治愈新增": [data.iloc[row]["治愈新增"]],
                #         "现存感染数": [data.iloc[row]["现存感染数"]],
                #         "现存增加数": [data.iloc[row]["现存增加数"]],
                #         "死亡人数": [data.iloc[row]["死亡人数"]],
                #         "新增死亡": [data.iloc[row]["新增死亡"]],
                #         "高风险地区数": [data.iloc[row]["高风险地区数"]],
                #         "中风险地区数": [data.iloc[row]["中风险地区数"]],
                #         "疑似总数": [data.iloc[row]["疑似总数"]],
                #         "新增疑似": [data.iloc[row]["新增疑似"]]
                #     }))
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
