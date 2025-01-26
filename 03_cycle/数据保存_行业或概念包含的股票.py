import akshare as ak
import datetime as dt
import pandas as pd
import time
from utils_cycle import *

# 保存行业或者概念下股票
trade_date = '20250124'
save_industry_file = '../01_save_data/industry_stock/' + trade_date
save_concept_file = '../01_save_data/concept_stock/' + trade_date
time_sleep = 0.3

industry_list = ak.stock_board_industry_name_em()
concept_list = ak.stock_board_concept_name_em()

for name in list(industry_list['板块名称']):
    print('行业: ', name)
    try:
        industry_stock = ak.stock_board_industry_cons_em(name)
        export_industry_or_concept_stock(save_industry_file, trade_date, name, industry_stock, 'stock')

        time.sleep(time_sleep)
    except:
        print('stock_board_industry_cons_em error: ', name)

for name in list(concept_list['板块名称']):
    print('概念: ', name)
    try:
        concept_stocks = ak.stock_board_concept_cons_em(name)
        # print(concept_stocks)
        if name in ('DRG/DIP'):
            export_industry_or_concept_stock(save_concept_file, trade_date, 'DRG', concept_stocks, 'stock')
        else:
            export_industry_or_concept_stock(save_concept_file, trade_date, name, concept_stocks, 'stock')

    except:
        print('stock_board_concept_cons_em error: ', name)
