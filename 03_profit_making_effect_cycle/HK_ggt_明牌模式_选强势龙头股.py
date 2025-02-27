import time
import akshare as ak
import numpy as np
from numpy import empty
import pandas as pd
import datetime as dt

# 处理时间
from dateutil.parser import parse
from datetime import datetime, timedelta
from chinese_calendar import is_workday, is_holiday

from utils_cycle import *

## 全局参数
debug_num = 20000
# action_date = dt.date.today()
action_date = '2025-02-21'
save_file = '../01_save_data/stock_HK/stock_HK_2025_02_21'

## 港股通成份股
stock_list = ak.stock_hk_ggt_components_em()
stock_symbol = stock_list['代码'].values
stock_name = stock_list['名称'].values
stocks_code = list(zip(stock_symbol, stock_name))
# stocks_code = ggt_all
print('**** 01 股票共计:', len(stocks_code), stocks_code)

## 召回
# 个股日线、周线、月线
print('*' * 50 + ' 03 召回数据')
stock_daily, stock_weekly, stock_monthly = {}, {}, {}
for i in range(min(len(stocks_code), debug_num)):
    try:
        print('**** load K line : ', stocks_code[i][0])
        stock_daily[stocks_code[i][0]], stock_weekly[stocks_code[i][0]], stock_monthly[stocks_code[i][0]] = \
            load_stocks(save_file, action_date, stocks_code[i][0])

        # print(stock_daily[stocks_code[i][0]][['日期', '收盘', '成交量']])
        # print(stock_weekly[stocks_code[i][0]][['日期', '收盘', '成交量']])
        # print(stock_monthly[stocks_code[i][0]][['日期', '收盘', '成交量']])
    except:
        print('**** has no day week month K line: ', stocks_code[i][0])
print('*' * 50 + ' 03 召回数据完毕')


def in_up_critical(df, N_days):
    # print(df.iloc[-1 - N_days:-1, 1].mean(), df.iloc[-1, 1])
    return df.iloc[-1, 1] / df.iloc[-1 - N_days:-1, 1].max()


def limit_up_many_times(df, ob_window_N_days, ob_thres=5.0):
    # print(df.iloc[-1 * ob_window_N_days:, 1])
    # print((df.iloc[-1 * ob_window_N_days:, 1] > ob_thres).sum())
    return (df.iloc[-1 * ob_window_N_days:, 1] > ob_thres).sum()


# 60日新高
new_high_in_N_days = 60
critical_thres_low = 0.95
# 近期多次涨停
ob_window_N_days = 10
ob_thres = 5.0
limit_up_times_thres = 1
# 60日新高且近期多次涨停 上面的合集

list_new_high, list_limit_up, list_total = [], [], []
for i in range(min(len(stocks_code), debug_num)):
    if stocks_code[i][0] == '09699': continue
    df = stock_daily[stocks_code[i][0]]

    # 60日新高
    up_critical_rate = in_up_critical(df[['日期', '收盘']], new_high_in_N_days)
    is_new_high_in_N_days = up_critical_rate > critical_thres_low

    # 近期多次涨停
    limit_up_times = limit_up_many_times(df[['日期', '涨跌幅']], ob_window_N_days, ob_thres)
    is_limit_up_many_times = limit_up_times > limit_up_times_thres

    if is_new_high_in_N_days:
        list_new_high.append([stocks_code[i][0], stocks_code[i][1], up_critical_rate])
        list_new_high.sort(key=lambda x: x[2], reverse=True)
    if is_limit_up_many_times:
        list_limit_up.append([stocks_code[i][0], stocks_code[i][1], limit_up_times])
        list_limit_up.sort(key=lambda x: x[2], reverse=True)
    if is_new_high_in_N_days and is_limit_up_many_times:
        list_total.append([stocks_code[i][0], stocks_code[i][1], limit_up_times])
        list_total.sort(key=lambda x: x[2], reverse=True)

print('日期: ', action_date, ', 往前看几天: ', ob_window_N_days, ', 阈值: ', ob_thres)
print('60日新高且近期多次涨停')
print(len(list_total), list_total)
print('60日新高')
print(len(list_new_high), list_new_high)
print('近期多次涨停')
print(len(list_limit_up), list_limit_up)
