import plotly as py
import plotly.graph_objects as go
import pandas as pd
import numpy as np

pyplt = py.offline.plot

url = "疫情大数据分析\\爬虫数据\\全国数据.csv"
data = pd.read_csv(url)
Start = str(data["日期"][data["日期"].argmin()])
End = str(data["日期"][data["日期"].argmax()])
date = pd.date_range(start=Start, end=End)

figure = go.Figure()
# haha=data["确诊总数"].to_list()
# print(haha)
# 对绘图添加 traces
trace1 = go.Scatter(x=date,
                    y=data["确诊总数"].to_list(),
                    marker=dict(color="#FFC125"),
                    mode="lines+markers",
                    name="确诊",
                    xaxis="x2",
                    yaxis="y2")
trace2 = go.Scatter(x=date,
                    y=data["疑似总数"].to_list(),
                    marker=dict(color="#FF0000"),
                    name="疑似",
                    mode="lines+markers",
                    xaxis="x2",
                    yaxis="y2")
trace3 = go.Scatter(x=date,
                    y=data["治愈总数"].to_list(),
                    marker=dict(color="#ADFF2F"),
                    name="治愈",
                    mode="lines+markers",
                    xaxis="x2",
                    yaxis="y2")
trace4 = go.Scatter(x=date,
                    y=data["死亡人数"].to_list(),
                    marker=dict(color="#1E1E1E"),
                    name="死亡",
                    mode="lines+markers",
                    xaxis="x2",
                    yaxis="y2")
trace5 = go.Scatter(x=date,
                    y=data["今日确诊数"].to_list(),
                    marker=dict(color="#FFC125"),
                    mode="lines+markers",
                    name="新增确诊",
                    xaxis="x",
                    yaxis="y")
trace6 = go.Scatter(x=date,
                    y=data["新增疑似"].to_list(),
                    marker=dict(color="#FF0000"),
                    name="新增疑似",
                    mode="lines+markers",
                    xaxis="x",
                    yaxis="y")
trace7 = go.Scatter(x=date,
                    y=data["治愈新增"].to_list(),
                    marker=dict(color="#ADFF2F"),
                    name="新增治愈",
                    mode="lines+markers",
                    xaxis="x",
                    yaxis="y")
trace8 = go.Scatter(x=date,
                    y=data["新增死亡"].to_list(),
                    marker=dict(color="#1E1E1E"),
                    name="新增死亡",
                    mode="lines+markers",
                    xaxis="x",
                    yaxis="y")

figure.add_traces([trace1, trace2, trace3, trace4])
figure.add_traces([trace5, trace6, trace7, trace8])

figure["layout"]["xaxis2"] = {}
figure["layout"]["yaxis2"] = {}

figure.layout.yaxis.update({"domain": [0, .45]})
figure.layout.yaxis2.update({"domain": [.6, 1.]})

figure.layout.yaxis2.update({"title": "人数"})
figure.layout.yaxis.update({"title": "人数"})
figure.layout.xaxis2.update({"title": "日期"})
figure.layout.xaxis.update({"title": "日期"})
figure.layout.update({"height": 900})
figure.update_layout(title_text="疫情趋势图", )
figure.update_layout(
    hovermode="x",
    template="plotly_white",
)

pyplt(figure, filename="疫情大数据分析\\网址\\折线图.html", show_link=False)
