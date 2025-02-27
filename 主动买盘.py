import akshare as ak
import pandas as pd

import datetime as dt

# 获取当前日期和时间
now = dt.datetime.now()
# 格式化输出时间，格式为年-月-日 时:分:秒
print(now.strftime("%Y-%m-%d %H:%M:%S"))

# real_time_data = ak.stock_zh_a_hist_pre_min_em()
# print(real_time_data)