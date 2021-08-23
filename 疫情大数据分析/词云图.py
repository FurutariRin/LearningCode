import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

path = "爬虫数据\\省份最新数据统计.csv"
wc = WordCloud(
    font_path=
    "C:\\Users\\FurutariRin\\AppData\\Local\\Microsoft\\Windows\\Fonts\\SourceHanSansCN-Bold.otf",
    background_color="#000000")
f = pd.read_csv(path, encoding="utf-8")
name = f["省份"].to_list()
value = f["确诊总数"].to_list()
for i in range(len(name)):
    name[i] = str(name[i])
dic = dict(zip(name, value))
wc.generate_from_frequencies(dic)
plt.imshow(wc)
plt.axis("off")
# plt.show()
wc.to_file("Project2\\图\\词云图.png")
