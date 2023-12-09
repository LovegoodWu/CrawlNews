# 导入需要的模块
import os
import requests
from bs4 import BeautifulSoup
import datetime

headers = {
    "Host": "www.guancha.cn",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.guancha.cn/",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cookie": "sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22189b3a05a562-015acfbff283e5e-1a525634-2073600-189b3a05a57a10%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22%24device_id%22%3A%22189b3a05a562-015acfbff283e5e-1a525634-2073600-189b3a05a57a10%22%7D; _v_=703528",
}

min_attention = 100000
min_comment = 100

# 定义要爬取的网址
url = "https://www.guancha.cn/internation?s=dhguoji"

response = requests.get(url, headers=headers)
html = response.text

# 解析网页内容，使用BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# 找到所有的文章列表项，使用find_all方法
# items = soup.find_all("h4", class_="module-title")
ul = soup.find_all("li")

# 获取今天日期
today_date = datetime.datetime.now().strftime("%Y-%m-%d")

# 创建文件夹
folder_name = f"News/{today_date}"
os.makedirs(folder_name, exist_ok=True)

# 遍历每一个列表项，获取需要的信息
for li in ul:
    h4 = li.find("h4", class_="module-title")
    if h4 is None:
        continue

    link = h4.find("a").get("href")
    if link is None or link == "":
        continue

    attention_count = int(li.select_one('.interact-attention').text)
    comment_count = int(li.select_one('.interact-comment').text)
    if attention_count < min_attention or comment_count < min_comment:
        continue

    link = "https://www.guancha.cn" + link
    article_response = requests.get(link, headers=headers)
    article_html = article_response.text
    article_soup = BeautifulSoup(article_html, "html.parser")
    article_title = article_soup.find("h3").get_text()

    formatted_preview = f"标题: {article_title}, 阅读量: {attention_count}, 评论量：{comment_count}"
    print(formatted_preview)

    article_contents = article_soup.find("div", class_="content all-txt").select(
        'p:not([style]):not([align]):not(p img):not(p span):not(p iframe):not(p:has(strong))')

    article = formatted_preview + "\n"
    for content in article_contents:
        article += content.get_text(strip=True)

    # 文件名不能包含特殊字符，替换掉不合法字符
    invalid_chars = '<>:"/\|?*'
    for char in invalid_chars:
        article_title = article_title.replace(char, '_')

    # 构建文件路径
    file_path = os.path.join(folder_name, f"{article_title}.txt")

    # 保存文本到文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(article)

# 输出提示信息，表示爬虫完成
print("\n爬虫完成，已将数据保存至" + f"{folder_name}")
