![][py3x] [![GitHub stars][stars]][stargazers] [![GitHub forks][forks]][network] [![GitHub issues][issues]][issues_url] [![GitHub license][license]][lic_file]

# V2EX_Crawler
Scrapy 爬取 V2EX 最近的文章, 存储到 Mongodb

# Features

- [x] 分页抓取 [V2EX Recent](https://www.v2ex.com/recent)
    - 相关用户, 及评论  
- [x] 存储数据到本地 MongoDB
- [x] 随机 User-Agent
- [x] 代理 IP

# Requirements
- Python 3.x
- MongoDB
- [V2EX](https://www.v2ex.com) 账号

# Usage
0. Python 3
1. 配置好本地 Mongodb
1. 首先在 `settings.py` 配置 MongoDB 的 uri 和 V2EX 的账户

```
MONGO_URI = "mongodb://localhost:27017"
MONGO_DATABASE = "V2EX"

V2EX_USERNAME = "xxx@gmail.com"
V2EX_PASSWORD = "xxx"
```

# Installation

1. `cd V2EX_Crawler`
2. `pip3 install -r requirements.txt`
3. `python3 main.py`

# Contact

Email : iShawnWang2333@gmail.com
Weibo : [王大屁帅2333](https://weibo.com/p/1005052848310723/home?from=page_100505&mod=TAB#place)

# License

V2EX_Cralwer is released under the GPL v3.0 license. See [LICENSE](https://github.com/iShawnWang/V2EX_Crawler/blob/master/LICENSE) for details.

[forks]: https://img.shields.io/github/forks/iShawnWang/V2EX_Crawler.svg[network]: https://github.com/iShawnWang/V2EX_Crawler/network

[stars]: https://img.shields.io/github/stars/iShawnWang/V2EX_Crawler.svg[stargazers]: https://github.com/iShawnWang/V2EX_Crawler/stargazers

[issues]:https://img.shields.io/github/issues/iShawnWang/V2EX_Crawler.svg
[issues_url]:https://github.com/iShawnWang/V2EX_Crawler/issues

[issues_img]: https://img.shields.io/github/issues/iShawnWang/V2EX_Crawler.svg[issues]: https://github.com/iShawnWang/V2EX_Crawler/issues

[py3x]:https://img.shields.io/badge/python-3.x-brightgreen.svg

[license]:https://img.shields.io/badge/license-GPL%20V3-red.svg

[lic_file]:https://raw.githubusercontent.com/xiyouMc/WebHubBot/master/LICENSE




