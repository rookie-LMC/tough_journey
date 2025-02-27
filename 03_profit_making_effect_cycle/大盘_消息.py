import akshare as ak

# 韭圈 恐惧贪婪指数表
# https://funddb.cn/tool/fear
# 金融市场的投资决策受到两种情绪的驱动，恐惧和贪婪。过度贪婪会让投资者把股价哄抬过高，过度恐惧会让股价跌破其应有的水平。
# 那么现在市场由哪种情绪主导？韭圈儿的恐惧贪婪指数可以帮助你快速识别，我们观察6大指标。
# 市场波动率。50etf期权波动率，这个是利用期权市场的特性来反应股票市场情绪的一个指标。
# 外资对A股的认可度。陆股通累计买入成交净额，偏离20日均线的程度。
# 股指期货年化升贴水率。采用沪深300股指（次月、10日平均）期货升贴水率。
# 股价强度。股市中创过去一年股价新高的股票个数占比。
# 避险需求。过去20个交易日中，股票回报率与债券回报率的差值，沪深300回报率-国债净价指数回报率。
# 杠杆率。A股融资买入金额占总成交金额的占比。（由于数据获取延迟，暂时不纳入统计）
# 针对每个指标，我们观察相对于其平均水平的偏离程度，并赋予0-100的分值，分值越高代表投资者越贪婪，50为中立。最后我们把所有的指标进行平均（等权）得到最终的指标。
index_fear_greed_funddb_df = ak.index_fear_greed_funddb(symbol="上证指数")
print('韭圈 恐惧贪婪指数表: https://funddb.cn/tool/fear')
print(index_fear_greed_funddb_df)

print('*' * 30)

# 数库-A股新闻情绪指数
# https://www.chinascope.com/reasearch.html
index_news_sentiment_scope_df = ak.index_news_sentiment_scope()
print('数库-A股新闻情绪指数: https://www.chinascope.com/reasearch.html')
print(index_news_sentiment_scope_df)

# stock_info_global_cls_df = ak.stock_info_cjzc_em()
stock_info_global_cls_df = ak.stock_info_global_em()
print(stock_info_global_cls_df.columns)
print(stock_info_global_cls_df[['标题', '发布时间']])


from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


def stock_info_global_em_v1() -> pd.DataFrame:
    """
    东方财富-全球财经快讯
    https://kuaixun.eastmoney.com/7_24.html
    :return: 全球财经快讯
    :rtype: pandas.DataFrame
    """
    url = "https://np-weblist.eastmoney.com/comm/web/getFastNewsList"
    params = {
        "client": "web",
        "biz": "web_724",
        "fastColumn": "102",
        "sortEnd": "",
        "pageSize": "300",
        "req_trace": "1710315450384",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    print(data_json)
    temp_df = pd.DataFrame(data_json["data"]["fastNewsList"])
    temp_df = temp_df[["title", "summary", "showTime", "code", 'titleColor']]
    temp_df["code"] = [
        f"https://finance.eastmoney.com/a/{item}.html" for item in temp_df["code"]
    ]
    temp_df.rename(
        columns={
            "title": "标题",
            "summary": "摘要",
            "showTime": "发布时间",
            "code": "链接",
            "titleColor": '中'
        },
        inplace=True,
    )
    return temp_df

stock_info_global_cls_df = stock_info_global_em_v1()
print(stock_info_global_cls_df.columns)
print(stock_info_global_cls_df[['标题', '发布时间', '中']])

