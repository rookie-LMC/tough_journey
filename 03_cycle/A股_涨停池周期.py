'''
Desc: 首页-行情中心-涨停板行情-涨停股池
https://quote.eastmoney.com/ztb/detail#type=ztgc

涨停板行情专题为您展示了 6 个股票池，分别为：
1. 涨停股池：包含当日当前涨停的所有A股股票(不含未中断连续一字涨停板的新股)；
2. 昨日涨停股池：包含上一交易日收盘时涨停的所有A股股票(不含未中断连续一字涨停板的新股)；
3. 强势股池：包含创下60日新高或近期多次涨停的A股股票；
4. 次新股池：包含上市一年以内且中断了连续一字涨停板的A股股票；
5. 炸板股池：包含当日触及过涨停板且当前未封板的A股股票；
6. 跌停股池：包含当日当前跌停的所有A股股票。
注：涨停板行情专题统计不包含ST股票及科创板股票。

A_daily_limit_up_market
'''

import akshare as ak
import datetime as dt
from utils_cycle import *

save_zt_file = '../01_save_data/A_daily_limit_up_market'
get_date = '20250117'
save_industry_file = '../01_save_data/industry_stock/' + get_date
save_concept_file = '../01_save_data/concept_stock/' + get_date

trade_date_list = ['20250117', '20250116', '20250115', '20250114', '20250113', '20250110', '20250109', '20250108',
                   '20250107', '20250106']
# trade_date_list = ['20250107']

# # 东方财富网-行情中心-涨停板行情-涨停股池
# df_zt = ak.stock_zt_pool_em(date=trade_date)
# # 东方财富网-行情中心-涨停板行情-昨日涨停股池
# df_zt_pvs = ak.stock_zt_pool_previous_em(date=trade_date)
# # 东方财富网-行情中心-涨停板行情-强势股池
# df_zt_strong = ak.stock_zt_pool_strong_em(date=trade_date)
# # 东方财富网-行情中心-涨停板行情-次新股池
# df_zt_sn = ak.stock_zt_pool_sub_new_em(date=trade_date)
# # 东方财富网-行情中心-涨停板行情-炸板股池
# df_zt_zbgc = ak.stock_zt_pool_zbgc_em(date=trade_date)
# # 东方财富网-行情中心-涨停板行情-跌停股池
# df_zt_dtgc = ak.stock_zt_pool_dtgc_em(date=trade_date)

industry_date, concept_date = {}, {}
industry_stock, concept_stock = {}, {}

industry_list = ak.stock_board_industry_name_em()
concept_list = ak.stock_board_concept_name_em()

for name in list(industry_list['板块名称']):
    try:
        df = load_industry_or_concept_stock(save_industry_file, get_date, name, 'stock')
        print('load_industry: ', name)
        industry_stock[name] = df
    except:
        print('load_industry error: ', name)

for name in list(concept_list['板块名称']):
    try:
        if name in ('DRG/DIP'):
            df = load_industry_or_concept_stock(save_concept_file, get_date, 'DRG', 'stock')
        else:
            df = load_industry_or_concept_stock(save_concept_file, get_date, name, 'stock')

        concept_stock[name] = df
        print('load_concept: ', name)
    except:
        print('load_concept error: ', name)

for trade_date in trade_date_list:
    df_zt, df_zt_pvs, df_zt_strong, df_zt_sn, df_zt_zbgc, df_zt_dtgc = load_zt_stocks(save_zt_file, trade_date)

    # 序号-代码-名称
    df_market = df_zt_strong
    print(df_market)
    stock_zt_list = get_stocks_code(df_market)
    print(stock_zt_list)
    stocks_code_industry_concept, num_industry, num_concept = get_industry_and_concept_of_stocks(stock_zt_list)

    industry_dic, concept_dic = group_and_sort(stocks_code_industry_concept)
    industry_date[trade_date], concept_date[trade_date] = industry_dic, concept_dic

print(industry_date)
print(concept_date)

print()
print('* ' * 30)
for trade_date in trade_date_list:
    print('* ' * 3, trade_date, '* ' * 3, ', 行业--数量排序')
    tmp = sorted(industry_date[trade_date].items(), key=lambda x: x[1], reverse=True)
    print(tmp)

print()
print('* ' * 30)
for trade_date in trade_date_list:
    print('* ' * 3, trade_date, '* ' * 3, ', 行业--比例排序')
    tmp = sorted(industry_date[trade_date].items(), key=lambda x: x[1], reverse=True)
    tmp_1 = [
        [i[0], i[1], i[1] * 1.0 / num_industry[i[0]], num_industry[i[0]]
         ] for i in tmp]
    print(sorted(tmp_1, key=lambda x: x[2], reverse=True))

print()
print('* ' * 30)
for trade_date in trade_date_list:
    print('* ' * 3, trade_date, '* ' * 3, ', 概念--数量排序')
    tmp = sorted(concept_date[trade_date].items(), key=lambda x: x[1], reverse=True)
    print(tmp)

print()
print('* ' * 30)
for trade_date in trade_date_list:
    print('* ' * 3, trade_date, '* ' * 3, ', 概念--比例排序')
    tmp = sorted(concept_date[trade_date].items(), key=lambda x: x[1], reverse=True)
    tmp_1 = [
        [i[0], i[1], i[1] * 1.0 / num_concept[i[0]], num_concept[i[0]]
         ] for i in tmp]
    print(sorted(tmp_1, key=lambda x: x[2], reverse=True))
