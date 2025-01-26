import akshare as ak
import datetime as dt
from utils_cycle import *

save_file = '../01_save_data/A_daily_limit_up_market'
trade_date = '20250124'

# 东方财富网-行情中心-涨停板行情-涨停股池
df_zt = ak.stock_zt_pool_em(date=trade_date)

# 东方财富网-行情中心-涨停板行情-昨日涨停股池
df_zt_pvs = ak.stock_zt_pool_previous_em(date=trade_date)

# 东方财富网-行情中心-涨停板行情-强势股池
df_zt_strong = ak.stock_zt_pool_strong_em(date=trade_date)

# 东方财富网-行情中心-涨停板行情-次新股池
df_zt_sn = ak.stock_zt_pool_sub_new_em(date=trade_date)

# 东方财富网-行情中心-涨停板行情-炸板股池
df_zt_zbgc = ak.stock_zt_pool_zbgc_em(date=trade_date)

# 东方财富网-行情中心-涨停板行情-跌停股池
df_zt_dtgc = ak.stock_zt_pool_dtgc_em(date=trade_date)

print(df_zt_dtgc.dtypes)

df_dic = {
    '涨停股池': df_zt,
    '昨日涨停股池': df_zt_pvs,
    '强势股池': df_zt_strong,
    '次新股池': df_zt_sn,
    '炸板股池': df_zt_zbgc,
    '跌停股池': df_zt_dtgc
}
export_df_dic(save_file, trade_date, df_dic)
