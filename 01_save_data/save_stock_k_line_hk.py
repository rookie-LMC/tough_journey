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

from utils_save import *

## 全局参数
debug_num = 200000000
sleep_time_day_week_month_info = 0.3
action_date = dt.date.today()
start_date = '20230101'
save_file = './stock_HK/stock_HK_2025_01_27'

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
        stock_daily[stocks_code[i][0]] = ak.stock_hk_hist(stocks_code[i][0], adjust="qfq", period="daily",
                                                          start_date=start_date)
        stock_weekly[stocks_code[i][0]] = ak.stock_hk_hist(stocks_code[i][0], adjust="qfq", period="weekly",
                                                           start_date=start_date)
        stock_monthly[stocks_code[i][0]] = ak.stock_hk_hist(stocks_code[i][0], adjust="qfq", period="monthly",
                                                            start_date=start_date)
        export_stocks(save_file, stock_daily[stocks_code[i][0]], stock_weekly[stocks_code[i][0]],
                      stock_monthly[stocks_code[i][0]],
                      action_date, stocks_code[i][0])
        time.sleep(sleep_time_day_week_month_info)
    except:
        print('**** has no day week month K line: ', stocks_code[i][0])
print('*' * 50 + ' 03 召回数据完毕')
