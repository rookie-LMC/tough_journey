import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.table import Table
from matplotlib.font_manager import FontProperties
import akshare as ak
import datetime as dt

# 中文显示
font_path = '/Users/limengchen03/SimHei.ttf'
font = FontProperties(fname=font_path)

start_time = time.time()

## 港股通成份股
stock_list = ak.stock_hk_ggt_components_em()
stock_symbol = stock_list['代码'].values
stock_name = stock_list['名称'].values
stocks_code = list(zip(stock_symbol, stock_name))
print('**** 01 股票共计:', len(stocks_code))

## 参数
start_date = '20240501'
debug_num = 4000000
sleep_time = 1

while True:
    start_time = time.time()
    print('*' * 10, start_time, '*' * 10)

    # 用于存储每天创 5、10、20 日新高的股票数量
    new_high_5d_count = {}
    new_high_10d_count = {}
    new_high_15d_count = {}
    new_high_20d_count = {}
    new_high_30d_count = {}
    new_high_60d_count = {}

    for i in range(min(len(stocks_code), debug_num)):
        try:
            # print('**** load K line : ', stocks_code[i][0])
            hk_df = ak.stock_hk_hist(symbol=stocks_code[i][0], adjust="qfq", period="daily",
                                     start_date=start_date)
            if len(hk_df) >= 60:
                for j in range(60, len(hk_df)):
                    date = hk_df.iloc[j]['日期']
                    close_price = hk_df.iloc[j]['收盘']

                    # 5 日新高判断
                    recent_5 = hk_df.iloc[j - 5:j]
                    if close_price > recent_5['收盘'].max():
                        if date in new_high_5d_count:
                            new_high_5d_count[date] += 1
                        else:
                            new_high_5d_count[date] = 1

                    # 10 日新高判断
                    recent_10 = hk_df.iloc[j - 10:j]
                    if close_price > recent_10['收盘'].max():
                        if date in new_high_10d_count:
                            new_high_10d_count[date] += 1
                        else:
                            new_high_10d_count[date] = 1

                    # 15 日新高判断
                    recent_15 = hk_df.iloc[j - 15:j]
                    if close_price > recent_15['收盘'].max():
                        if date in new_high_15d_count:
                            new_high_15d_count[date] += 1
                        else:
                            new_high_15d_count[date] = 1

                    # 20 日新高判断
                    recent_20 = hk_df.iloc[j - 20:j]
                    if close_price > recent_20['收盘'].max():
                        if date in new_high_20d_count:
                            new_high_20d_count[date] += 1
                        else:
                            new_high_20d_count[date] = 1

                    # 30 日新高判断
                    recent_30 = hk_df.iloc[j - 30:j]
                    if close_price > recent_30['收盘'].max():
                        if date in new_high_30d_count:
                            new_high_30d_count[date] += 1
                        else:
                            new_high_30d_count[date] = 1

                    # 60 日新高判断
                    recent_60 = hk_df.iloc[j - 60:j]
                    if close_price > recent_60['收盘'].max():
                        if date in new_high_60d_count:
                            new_high_60d_count[date] += 1
                        else:
                            new_high_60d_count[date] = 1

            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error occurred while fetching data for {stocks_code[i][0]}: {e}")

    # 将结果转换为 DataFrame
    new_high_5d_df = pd.DataFrame.from_dict(new_high_5d_count, orient='index', columns=['5 日新高数量'])
    new_high_10d_df = pd.DataFrame.from_dict(new_high_10d_count, orient='index', columns=['10 日新高数量'])
    new_high_15d_df = pd.DataFrame.from_dict(new_high_15d_count, orient='index', columns=['15 日新高数量'])
    new_high_20d_df = pd.DataFrame.from_dict(new_high_20d_count, orient='index', columns=['20 日新高数量'])
    new_high_30d_df = pd.DataFrame.from_dict(new_high_30d_count, orient='index', columns=['30 日新高数量'])
    new_high_60d_df = pd.DataFrame.from_dict(new_high_60d_count, orient='index', columns=['60 日新高数量'])

    # 合并结果
    result_df = pd.concat([new_high_5d_df, new_high_10d_df, new_high_15d_df,
                           new_high_20d_df, new_high_30d_df, new_high_60d_df], axis=1)
    result_df = result_df.sort_index()

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print('5、10、15、20、30、60 日新高的股票数量: ')
    print(result_df)

    end_time = time.time()
    print(f"代码执行时间为: {end_time - start_time} 秒")
