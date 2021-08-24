import pandas as pd
import csv
from tqdm import tqdm

filePath = "疫情大数据分析\\爬虫数据\\全国死亡率与治愈率.csv"
f = open(filePath, "w", encoding="utf-8", newline="")
csv_writer = csv.writer(f)
csv_writer.writerow(["日期", "确诊总数", "治愈总数", "死亡人数",
                    "感染死亡率", "感染治愈率", "住院死亡率", "住院治愈率"])
UseData=pd.read_csv("疫情大数据分析\\爬虫数据\\全国数据.csv")
for i in tqdm(range(len(UseData)),desc="计算死亡率与治愈率",unit="Day"):
    Date=UseData.iloc[i]["日期"]