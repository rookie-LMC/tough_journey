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

from utils_select import *

## 全局参数
debug_num = 2000000000
# action_date = dt.date.today()
action_date = '2025-01-17'
save_file = '../01_save_data/stock_HK/stock_HK_2025_01_17'

## 港股通成份股
stock_list = ak.stock_hk_ggt_components_em()
stock_symbol = stock_list['代码'].values
stock_name = stock_list['名称'].values
stocks_code = list(zip(stock_symbol, stock_name))
print('**** 01 股票共计:', len(stocks_code))

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


## 选股
# 在250日均线上 完成
# 股价在30元以下 完成
# 流通股份要在30亿以内 搁置
# 月线至少看3根，两阳夹一阴，上升趋势的双阳夹阴,做突破这三根月线的最高点（注意月线是否上升趋势，近期涨幅太大的都不要摆在首选，次选可以）
# 65天内有过涨停的票（首板不值得去追，但是有了这个首板就可以开始关注了，主力资金先把股价拉起来，接下来就是洗盘做量（过程有长有短）然后才是真正的突破（也可能中间重复一次洗盘），这个过程大概是三个月）

def greater_than_n_days_mean_price(df, n_days=250):
    # print(df.iloc[-1, 0], df.iloc[-1, 1])
    # print(df.iloc[-1 * n_days:, 1].mean())
    return df.iloc[-1, 1] > df.iloc[-1 * n_days:, 1].mean()


def less_than_target_price(df, target_price=30):
    # print(df.iloc[-1, 0], df.iloc[-1, 1])
    # print(df.iloc[-1 * n_days:, 1].mean())
    return df.iloc[-1, 1] < target_price


def has_limit_up_in_n_days(df, n_days=65, limit_up=9.9):
    # print(df.iloc[-1 * n_days:, :])
    # print(df.iloc[-1 * n_days:, 1].max())
    return df.iloc[-1 * n_days:, 1].max() > limit_up


def is_pos_line(close_price, open_price):
    # 收盘价高于开盘价的K线
    return close_price > open_price


def is_neg_line(close_price, open_price):
    # 收盘价低于开盘价时
    return close_price < open_price


def is_upward_trend(fir_low, sec_low, thr_low):
    return fir_low < sec_low and sec_low < thr_low


def month_pos_neg_pos_up_trend(df, stock_num, month_line_mode=4):
    # print(len(df))
    # 月线数量小于month_line_mode
    if len(df) < month_line_mode:
        print('月线数量不足: ', stock_num, ', month_line_mode: ', month_line_mode)

    # 旭东模式：月线至少看3根，上升趋势的双阳夹阴,只做第四个月
    if month_line_mode == 4:
        # 第一个月
        fir_stat = is_pos_line(df.iloc[-4, 1], df.iloc[-4, 2])
        # 第二个月
        sec_stat = is_neg_line(df.iloc[-3, 1], df.iloc[-3, 2])
        # 第三个月
        thr_stat = is_pos_line(df.iloc[-2, 1], df.iloc[-2, 2])
        # 上升趋势
        trend_stat = is_upward_trend(df.iloc[-4, 3], df.iloc[-3, 3], df.iloc[-2, 3])
    if month_line_mode == 3:
        # 第一个月
        fir_stat = is_pos_line(df.iloc[-3, 1], df.iloc[-3, 2])
        # 第二个月
        sec_stat = is_neg_line(df.iloc[-2, 1], df.iloc[-2, 2])
        # 第三个月
        thr_stat = is_pos_line(df.iloc[-1, 1], df.iloc[-1, 2])
        # 上升趋势
        trend_stat = is_upward_trend(df.iloc[-3, 3], df.iloc[-2, 3], df.iloc[-1, 3])

    return fir_stat and sec_stat and thr_stat and trend_stat


def in_up_critical(df_day, df_month, critical_thres_low, critical_thres_high, month_line_mode=4):
    day_val = df_day.iloc[-1, 1]
    month_val = 0
    if month_line_mode == 4:
        month_val = max(df_month.iloc[-4, 1], df_month.iloc[-3, 1], df_month.iloc[-2, 1])
    if month_line_mode == 3:
        month_val = max(df_month.iloc[-3, 1], df_month.iloc[-2, 1], df_month.iloc[-1, 1])

    # 最近一天收盘价 / 3根月线的最高价, 判断是否多头临界
    return day_val / month_val >= critical_thres_low and day_val / month_val <= critical_thres_high, day_val / month_val


select_stocks_code_with_thres = []
month_line_mode = 4
critical_thres_low, critical_thres_high = 0.90, 1.1
for i in range(min(len(stocks_code), debug_num)):
    try:
        # stock_data = stock_daily[stocks_code[i][0]][['日期', '收盘', '成交量']]
        # 股价在250日均线上
        # judger_1 = True
        judger_1 = greater_than_n_days_mean_price(stock_daily[stocks_code[i][0]][['日期', '收盘']],
                                                  250)
        # 股价在30元以下
        judger_2 = less_than_target_price(stock_daily[stocks_code[i][0]][['日期', '收盘']],
                                          50000)
        # 65天内有过涨停
        judger_3 = has_limit_up_in_n_days(stock_daily[stocks_code[i][0]][['日期', '涨跌幅']],
                                          65, 7.0)
        # 月线至少看3根，两阳夹一阴，上升趋势的双阳夹阴
        judger_4 = True
        # judger_4 = month_pos_neg_pos_up_trend(stock_monthly[stocks_code[i][0]][['日期', '收盘', '开盘', '最低']],
        #                                       stocks_code[i][0],
        #                                       month_line_mode)

        # 多头临界
        judger_5, critical_rate = in_up_critical(stock_daily[stocks_code[i][0]][['日期', '收盘']],
                                                 stock_monthly[stocks_code[i][0]][['日期', '最高']],
                                                 critical_thres_low,
                                                 critical_thres_high,
                                                 month_line_mode)

        if judger_1 and judger_2 and judger_3 and judger_4 and judger_5:
            print('满足筛选条件: ', stocks_code[i])
            select_stocks_code_with_thres.append([stocks_code[i], critical_rate])
    except:
        print('**** has no stock data K line: ', stocks_code[i][0])

print('*' * 50)
print('*' * 20 + ' 分析日期: ', action_date, ', 读取文件夹', save_file, ', 月线模式:', month_line_mode)
print('*' * 20 + ' 满足筛选条件的票', ', 多头临界区间', critical_thres_low, '~', critical_thres_high)
select_stocks_code_with_thres.sort(key=lambda x: x[1], reverse=True)
print([i[0] for i in select_stocks_code_with_thres])
for i in select_stocks_code_with_thres:
    print(i[0][0], i[0][1], i[1])
