import urllib.request as req
url = ("https://www.businesstoday.com.tw/article/category/183025/post/202203060007/"

with req.urlopen(url) as response:
    data = response.read().decode("utf-8")
print(data)