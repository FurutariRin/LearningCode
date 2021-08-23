import pandas as pd
import datetime
import time
from pyecharts.charts import Map
from pyecharts import options

# date = input("输入查询的日期：")


def getData(date: str):
    """
    获取当日数据\n
    param date 输入时间\n
    return 当日数据\n
    """
    AllData = []
    provinceData = pd.read_csv("爬虫数据\\代号意义.csv", encoding="utf-8")
    # 遍历所有省份
    for i in range(0, 33):
        # 省份对应文件
        filePath = "爬虫数据\\预处理数据\\" + str(i) + ".csv"
        # 读取文件
        data = pd.read_csv(filePath, encoding="utf-8")
        time_tuple = time.strptime(str(data["日期"][data["日期"].argmax()]),
                                   "%Y%m%d")
        year, month, day = time_tuple[:3]
        MaxDate = datetime.date(year, month, day)
        time_tuple = time.strptime(str(data["日期"][data["日期"].argmin()]),
                                   "%Y%m%d")
        year, month, day = time_tuple[:3]
        MinDate = datetime.date(year, month, day)
        # print(MaxDate)
        # print(MinDate)
        # print(len(data))
        dateTime = datetime.date(
            datetime.datetime.strptime(date, "%Y%m%d").year,
            datetime.datetime.strptime(date, "%Y%m%d").month,
            datetime.datetime.strptime(date, "%Y%m%d").day)
        while 1:
            row = 0
            for row in range(len(data)):
                if (str(data["日期"][row]) == date):
                    # inm = data.iloc[row]
                    # print(inm)
                    # print(provinceData.iloc[i,1])
                    Data = dict(province=provinceData.iloc[i, 1],
                                dateId=data.iloc[row]["日期"],
                                confirmedCount=data.iloc[row]["确诊总数"],
                                confirmedIncr=data.iloc[row]["今日确诊数"],
                                curedCount=data.iloc[row]["治愈总数"],
                                curedIncr=data.iloc[row]["治愈新增"],
                                currentConfirmedCount=data.iloc[row]["现存感染数"],
                                currentConfirmedIncr=data.iloc[row]["现存增加数"],
                                deadCount=data.iloc[row]["死亡人数"],
                                deadIncr=data.iloc[row]["新增死亡"],
                                highDangerCount=data.iloc[row]["高风险地区数"],
                                midDangerCount=data.iloc[row]["中风险地区数"],
                                suspectedCount=data.iloc[row]["疑似总数"],
                                suspectedCountIncr=data.iloc[row]["新增疑似"])
                    AllData.append(Data)
                    break
            if (str(data["日期"][row]) == date):
                break
            if (dateTime < MinDate):
                dateTime = MinDate
                date = MinDate.strftime("%Y%m%d")
            elif (dateTime > MaxDate):
                dateTime = MaxDate
                date = MaxDate.strftime("%Y%m%d")
            else:
                delta = datetime.timedelta(days=1)
                dateTime = dateTime - delta
    return AllData


date = input("输入查询的日期：")
data = getData(date)
currentConfirmedCount_data = []
currentConfirmedCount = 0
confirmedCount_data = []
confirmedCount = 0
for i in range(len(data)):
    currentConfirmedCount_data.append(
        (data[i]["province"], str(data[i]["currentConfirmedCount"])))
    currentConfirmedCount = currentConfirmedCount + data[i][
        "currentConfirmedCount"]
    confirmedCount_data.append(
        (data[i]["province"], str(data[i]["confirmedCount"])))
    confirmedCount = confirmedCount + data[i]["confirmedCount"]
# print(data[0]["province"])
#创建国家地图
map_country = Map()
#设置地图上的标题和数据标记，添加确诊人数
map_country.set_global_opts(
    title_opts=options.TitleOpts(title="中国实时疫情图" + "\n确诊人数" +
                                 str(confirmedCount) + "\n现存感染数：" +
                                 str(currentConfirmedCount)),
    visualmap_opts=options.VisualMapOpts(
        is_piecewise=True,  #设置是否为分段显示
        #自定义数据范围和对应的颜色
        pieces=[
            {
                "min": 1000,
                "label": '>1000人',
                "color": "#6F171F"
            },  # 不指定 max，表示 max 为无限大（Infinity）。
            {
                "min": 500,
                "max": 1000,
                "label": '500-1000人',
                "color": "#C92C34"
            },
            {
                "min": 100,
                "max": 499,
                "label": '100-499人',
                "color": "#E35B52"
            },
            {
                "min": 10,
                "max": 99,
                "label": '10-99人',
                "color": "#F39E86"
            },
            {
                "min": 1,
                "max": 9,
                "label": '1-9人',
                "color": "#FDEBD0"
            }
        ]))
#将数据添加进去，生成中国地图，所以maptype要对应china。
map_country.add("现存", currentConfirmedCount_data, maptype="china")
map_country.add("确诊", confirmedCount_data, maptype="china")
#一切完成，那么生成一个html网页文件。
map_country.render("Project2\\网址\\中国疫情数据.html")
