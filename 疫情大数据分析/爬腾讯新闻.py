import csv
import requests
from tqdm.std import tqdm

# 链接offset为新闻偏移量，limit为显示数量
url = "https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=antip&srv_id=pc&offset=0&limit=20&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:10,%22check_type%22:true}"
head = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
}
req = requests.get(url).json()
filePath = "爬虫数据\\新闻数据\\每日新闻.csv"
f = open(filePath, "w", encoding="utf-8")
csv_writer = csv.writer(f)
csv_writer.writerow(["新闻标题", "URL", "IMGURL", "作者", "发布时间"])
# print(len(req["data"]["list"]))
# print(req["data"]["list"][0]["url"])
for i in tqdm(range(len(req["data"]["list"])),desc="获取新闻数据",unit="条新闻"):
    csv_writer.writerow([
        req["data"]["list"][i]["title"], req["data"]["list"][i]["url"],
        req["data"]["list"][i]["img"], req["data"]["list"][i]["media_name"],
        req["data"]["list"][i]["publish_time"]
    ])
f.close()
