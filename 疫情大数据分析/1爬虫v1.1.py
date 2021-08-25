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
