import akshare as ak
import datetime as dt
import pandas as pd
import time
from utils_cycle import *

# 保存行业或者概念下股票
trade_date = '20250127'
save_industry_file = '../01_save_data/industry/' + trade_date
save_concept_file = '../01_save_data/concept/' + trade_date
time_sleep = 0.3
start_date = '20201201'
end_date = '20500101'

industry_list = ak.stock_board_industry_name_em()
concept_list = ak.stock_board_concept_name_em()

for name in list(industry_list['板块名称']):
    print('行业: ', name)
    try:
        df_day = ak.stock_board_industry_hist_em(symbol=name, start_date=start_date, end_date=end_date, period='日k',
                                                 adjust='qfq')
        df_week = ak.stock_board_industry_hist_em(symbol=name, start_date=start_date, end_date=end_date, period='周k',
                                                  adjust='qfq')
        df_month = ak.stock_board_industry_hist_em(symbol=name, start_date=start_date, end_date=end_date, period='月k',
                                                   adjust='qfq')

        df_dic = {
            'day': df_day,
            'week': df_week,
            'month': df_month,
        }
        export_df_dic_more(save_industry_file, trade_date, name, df_dic)
        time.sleep(time_sleep)
    except:
        print('stock_board_industry_cons_em error: ', name)

for name in list(concept_list['板块名称']):
    print('概念: ', name)
    try:
        df_day = ak.stock_board_concept_hist_em(symbol=name, start_date=start_date, end_date=end_date, period='daily',
                                                adjust='qfq')
        df_week = ak.stock_board_concept_hist_em(symbol=name, start_date=start_date, end_date=end_date, period='weekly',
                                                 adjust='qfq')
        df_month = ak.stock_board_concept_hist_em(symbol=name, start_date=start_date, end_date=end_date,
                                                  period='monthly',
                                                  adjust='qfq')

        df_dic = {
            'day': df_day,
            'week': df_week,
            'month': df_month,
        }
        if name in ('DRG/DIP'):
            export_df_dic_more(save_concept_file, trade_date, 'DRG', df_dic)
        else:
            export_df_dic_more(save_concept_file, trade_date, name, df_dic)
        time.sleep(time_sleep)
    except:
        print('stock_board_concept_cons_em error: ', name)

# name = 'DRG/DIP'
# df_day = ak.stock_board_concept_hist_em(symbol=name, start_date=start_date, end_date=end_date, period='daily',
#                                         adjust='qfq')
# df_week = ak.stock_board_concept_hist_em(symbol=name, start_date=start_date, end_date=end_date, period='weekly',
#                                          adjust='qfq')
# df_month = ak.stock_board_concept_hist_em(symbol=name, start_date=start_date, end_date=end_date,
#                                           period='monthly',
#                                           adjust='qfq')
# df_dic = {
#     'day': df_day,
#     'week': df_week,
#     'month': df_month,
# }
# export_df_dic_more(save_concept_file, trade_date, name, df_dic)
