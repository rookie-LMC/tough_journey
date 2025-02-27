import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.table import Table
from matplotlib.font_manager import FontProperties
import akshare as ak
import datetime as dt
from utils_cycle import *

# 中文显示
font_path = '/Users/limengchen03/SimHei.ttf'
font = FontProperties(fname=font_path)

start_time = time.time()

## 港股通成份股
stock_list = ak.stock_hk_ggt_components_em()
stock_symbol = stock_list['代码'].values
stock_name = stock_list['名称'].values
stocks_code = list(zip(stock_symbol, stock_name))
# stocks_code = ggt_all
print('**** 01 股票共计:', len(stocks_code))

## 参数
start_date = '20250201'
debug_num = 4000000
sleep_time = 0.1

while True:
    # 用于存储有溢价情况的股票信息
    premium_stocks = []
    prev_gain_thres, today_gain_thres = 3, 3
    for i in range(min(len(stocks_code), debug_num)):
        try:
            # print('**** load K line : ', stocks_code[i][0])
            hk_df = ak.stock_hk_hist(stocks_code[i][0], adjust="qfq", period="daily",
                                     start_date=start_date)
            # print(hk_df)
            if len(hk_df) >= 2:
                for j in range(1, len(hk_df)):
                    # 计算昨日涨幅
                    prev_gain = hk_df.iloc[j - 1]['涨跌幅']
                    # 计算今日涨幅
                    today_gain = hk_df.iloc[j]['涨跌幅']

                    # 判断昨日涨幅是否超过 5% 且今日涨幅也超过 5%
                    if prev_gain > prev_gain_thres and today_gain > today_gain_thres:
                        # print(stocks_code[i][0])
                        premium_stocks.append({
                            '股票代码': stocks_code[i][0],
                            '股票名称': stocks_code[i][1],
                            '昨日日期': hk_df.iloc[j - 1]['日期'],
                            '昨日涨幅': prev_gain,
                            '今日日期': hk_df.iloc[j]['日期'],
                            '今日涨幅': today_gain
                        })

            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error occurred while fetching data for {stocks_code[i][0]}: {e}")

    # 将结果转换为 DataFrame
    premium_df = pd.DataFrame(premium_stocks)

    # 统计每天的溢价数量
    daily_premium_count = premium_df.groupby('今日日期').size().reset_index(name='溢价数量')

    # 打印结果
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print("daily_premium_count: ")
    print(daily_premium_count)
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # 获取当前日期和时间, 格式化输出时间，格式为年-月-日 时:分:秒
    print('*' * 20)
