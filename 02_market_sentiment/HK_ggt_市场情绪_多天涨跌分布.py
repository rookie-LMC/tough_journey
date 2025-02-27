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
start_date = '20250210'
debug_num = 4000000
sleep_time = 0.1

while True:
    # 用于存储每天涨跌股票数量的字典
    start_time = time.time()
    # print('*' * 10, start_time, '*' * 10)
    daily_up_down_count, daily_up_down_detail_count, daily_up_down_detail_v1_count = {}, {}, {}

    for i in range(min(len(stocks_code), debug_num)):
        try:
            # print('**** load K line : ', stocks_code[i][0])
            hk_df = ak.stock_hk_hist(stocks_code[i][0], adjust="qfq", period="daily",
                                     start_date=start_date)
            for index, row in hk_df.iterrows():
                # print(index,row)
                date = row['日期']
                change_pct = row['涨跌幅']

                if date not in daily_up_down_count:
                    daily_up_down_count[date] = {'up': 0, 'down': 0}
                    daily_up_down_detail_count[date] = {
                        '10以上': 0,
                        '10~5': 0,
                        '5~2': 0,
                        '2~0': 0,
                        '0': 0,
                        '0~负2': 0,
                        '负2~负5': 0,
                        '负5~负10': 0,
                        '负10以下': 0
                    }
                    daily_up_down_detail_v1_count[date] = {
                        '10以上': 0,
                        '10~5': 0,
                        '负5~负10': 0,
                        '负10以下': 0
                    }

                if change_pct > 0:
                    daily_up_down_count[date]['up'] += 1
                elif change_pct < 0:
                    daily_up_down_count[date]['down'] += 1

                if change_pct >= 10:
                    daily_up_down_detail_count[date]['10以上'] += 1
                if change_pct < 10 and change_pct >= 5:
                    daily_up_down_detail_count[date]['10~5'] += 1
                if change_pct < 5 and change_pct >= 2:
                    daily_up_down_detail_count[date]['5~2'] += 1
                if change_pct < 2 and change_pct > 0:
                    daily_up_down_detail_count[date]['2~0'] += 1
                if change_pct == 0:
                    daily_up_down_detail_count[date]['0'] += 1
                if change_pct < 0 and change_pct >= -2:
                    daily_up_down_detail_count[date]['0~负2'] += 1
                if change_pct < -2 and change_pct >= -5:
                    daily_up_down_detail_count[date]['负2~负5'] += 1
                if change_pct < -5 and change_pct >= -10:
                    daily_up_down_detail_count[date]['负5~负10'] += 1
                if change_pct < -10:
                    daily_up_down_detail_count[date]['负10以下'] += 1

                if change_pct >= 10:
                    daily_up_down_detail_v1_count[date]['10以上'] += 1
                if change_pct < 10 and change_pct >= 5:
                    daily_up_down_detail_v1_count[date]['10~5'] += 1
                if change_pct < -5 and change_pct >= -10:
                    daily_up_down_detail_v1_count[date]['负5~负10'] += 1
                if change_pct < -10:
                    daily_up_down_detail_v1_count[date]['负10以下'] += 1

            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error occurred while fetching data for {stocks_code[i][0]}: {e}")

    # 将统计结果转换为DataFrame
    daily_up_down_df = pd.DataFrame.from_dict(daily_up_down_count, orient='index')
    daily_up_down_df.index = pd.to_datetime(daily_up_down_df.index)

    daily_up_down_detail_df = pd.DataFrame.from_dict(daily_up_down_detail_count, orient='index')
    daily_up_down_detail_df.index = pd.to_datetime(daily_up_down_detail_df.index)

    daily_up_down_detail_v1_df = pd.DataFrame.from_dict(daily_up_down_detail_v1_count, orient='index')
    daily_up_down_detail_v1_df.index = pd.to_datetime(daily_up_down_detail_v1_df.index)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print('daily_up_down_df: ')
    print(daily_up_down_df)
    print()
    print('daily_up_down_detail_df: ')
    print(daily_up_down_detail_df)
    print()
    print('daily_up_down_detail_v1_df: ')
    print(daily_up_down_detail_v1_df)

    end_time = time.time()
    print(f"代码执行时间为: {end_time - start_time} 秒")
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # 获取当前日期和时间, 格式化输出时间，格式为年-月-日 时:分:秒

    # 可视化每天股票涨跌分布
    # plt.figure(figsize=(12, 6))
    # plt.bar(daily_up_down_df.index, daily_up_down_df['up'], label='上涨股票数量', color='red')
    # plt.bar(daily_up_down_df.index, -daily_up_down_df['down'], label='下跌股票数量', color='green')
    # plt.xlabel('日期', fontproperties=font)
    # plt.ylabel('股票数量', fontproperties=font)
    # plt.title('港股通股票每日涨跌分布', fontproperties=font)
    # plt.legend(prop=font)
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.show()

'''
核对日期
2025-02-07
2025-02-11
'''
