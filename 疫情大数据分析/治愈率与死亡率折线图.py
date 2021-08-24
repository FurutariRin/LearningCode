import plotly as py
import plotly.graph_objects as go
import pandas as pd

pyplt = py.offline.plot

url = "疫情大数据分析\\爬虫数据\\全国死亡率与治愈率.csv"
data = pd.read_csv(url)
Start = str(data["日期"][data["日期"].argmin()])
End = str(data["日期"][data["日期"].argmax()])
date = pd.date_range(start=Start, end=End)

figure = go.Figure()

trace1 = go.Scatter(x=date, y=data["感染死亡率"].to_list(), marker=dict(color="#FFC125"), mode="lines+markers",
                    name="感染死亡率",
                    xaxis="x1",
                    yaxis="y1")
trace2 = go.Scatter(x=date, y=data["感染治愈率"].to_list(), marker=dict(color="#FF0000"), mode="lines+markers",
                    name="感染治愈率",
                    xaxis="x1",
                    yaxis="y1")
trace3 = go.Scatter(x=date, y=data["住院死亡率"].to_list(), marker=dict(color="#ADFF2F"), mode="lines+markers",
                    name="住院死亡率",
                    xaxis="x2",
                    yaxis="y2")
trace4 = go.Scatter(x=date, y=data["住院治愈率"].to_list(), marker=dict(color="#1E1E1E"), mode="lines+markers",
                    name="住院治愈率",
                    xaxis="x2",
                    yaxis="y2")

figure.add_traces([trace1, trace2])
figure.add_traces([trace3, trace4])

figure["layout"]["xaxis2"] = {}
figure["layout"]["yaxis2"] = {}

figure.layout.yaxis.update({"domain": [0, .45]})
figure.layout.yaxis2.update({"domain": [.6, 1.]})

figure.layout.yaxis2.update({"title": "比率"})
figure.layout.yaxis.update({"title": "比率"})
figure.layout.xaxis2.update({"title": "日期"})
figure.layout.xaxis.update({"title": "日期"})

figure.layout.update({"height": 900})
figure.update_layout(title_text="治愈率与死亡率", )
figure.update_layout(
    hovermode="x",
    template="plotly_white",
)

pyplt(figure, filename="疫情大数据分析\\网址\\治愈率与死亡率折线图.html", show_link=False)