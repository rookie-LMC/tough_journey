import akshare as ak
import pandas as pd
import time

time_sleep = 0.2

black_list = [
    [],
    [],
    [],
    [],
    [],
    [],
]


def get_stocks_code(df, code_col=2, name_col=3):
    stocks_code = []
    rows, cols = df.shape
    for row in range(rows):
        stocks_code.append([df.iloc[row, code_col], df.iloc[row, name_col]])
    return stocks_code


def get_industry_and_concept_of_stocks_v1(stocks_code, industry_stock, concept_stock, debug_num=20000):
    stocks_code_industry_concept, num_industry, num_concept = {}, {}, {}
    for i in range(min(len(stocks_code), debug_num)):
        st_code, st_name = stocks_code[i][0], stocks_code[i][1]
        stocks_code_industry_concept[st_code] = [[], [], st_name]

    for name, df in industry_stock.items():
        print(name)
        num_industry[name] = len(list(df[['代码']]))
        for i in range(min(len(stocks_code), debug_num)):
            st_code, st_name = stocks_code[i][0], stocks_code[i][1]

    for name, df in concept_stock.items():
        print(name)

    return stocks_code_industry_concept, num_industry, num_concept


def get_industry_and_concept_of_stocks(stocks_code, debug_num=20000):
    industry_list = ak.stock_board_industry_name_em()
    concept_list = ak.stock_board_concept_name_em()
    stocks_code_industry_concept, num_industry, num_concept = {}, {}, {}
    # print(industry_list)
    # print(concept_list)
    for i in range(min(len(stocks_code), debug_num)):
        st_code, st_name = stocks_code[i][0], stocks_code[i][1]
        stocks_code_industry_concept[st_code] = [[], [], st_name]

    for name in list(industry_list['板块名称']):
        print(name)
        try:
            industry_stock = ak.stock_board_industry_cons_em(name)
            num_industry[name] = len(list(industry_stock['代码']))
            # print([type(i) for i in industry_stock['代码']])
            for i in range(min(len(stocks_code), debug_num)):
                st_code, st_name = stocks_code[i][0], stocks_code[i][1]
                if st_code in list(industry_stock['代码']):
                    stocks_code_industry_concept[st_code][0].append(name)
                    # print('yes')

            time.sleep(time_sleep)
        except:
            print('stock_board_industry_cons_em error: ', name)

    for name in list(concept_list['板块名称']):
        print(name)
        try:
            concept_stocks = ak.stock_board_concept_cons_em(name)
            num_concept[name] = len(list(concept_stocks['代码']))
            for i in range(min(len(stocks_code), debug_num)):
                st_code, st_name = stocks_code[i][0], stocks_code[i][1]
                if st_code in list(concept_stocks['代码']):
                    stocks_code_industry_concept[st_code][1].append(name)
                    # print('yes')

            time.sleep(time_sleep)
        except:
            print('stock_board_concept_cons_em error: ', name)

    return stocks_code_industry_concept, num_industry, num_concept


def group_and_sort(target):
    industry_dic, concept_dic = {}, {}
    for key, val in target.items():
        industry, concept = val[0], val[1]
        for i in industry:
            industry_dic[i] = industry_dic.get(i, 0) + 1
        for i in concept:
            concept_dic[i] = concept_dic.get(i, 0) + 1
    return industry_dic, concept_dic


def export_df_dic(save_file, trade_date, df_dic):
    # 一天存一个
    file_path = save_file + '/' + str(trade_date) + '.xlsx'
    print(file_path)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for zt, df in df_dic.items():
            df.to_excel(writer, sheet_name=zt)


def export_df_dic_more(save_file, trade_date, industry_or_concept, df_dic):
    # 一天存多个
    file_path = save_file + '/' + str(trade_date) + '-' + str(industry_or_concept) + '.xlsx'
    print(file_path)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for zt, df in df_dic.items():
            df.to_excel(writer, sheet_name=zt)


def export_industry_or_concept_stock(save_file, trade_date, industry_or_concept, df, sheet_name):
    file_path = save_file + '/' + str(trade_date) + '-' + str(industry_or_concept) + '.xlsx'
    print(file_path)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name)


def load_zt_stocks(save_file, trade_date):
    file_path = save_file + '/' + str(trade_date) + '.xlsx'
    df_zt = pd.read_excel(file_path, sheet_name='涨停股池', dtype=str)
    print(df_zt.dtypes)
    df_zt_pvs = pd.read_excel(file_path, sheet_name='昨日涨停股池', dtype=str)
    df_zt_strong = pd.read_excel(file_path, sheet_name='强势股池', dtype=str)
    df_zt_sn = pd.read_excel(file_path, sheet_name='次新股池', dtype=str)
    df_zt_zbgc = pd.read_excel(file_path, sheet_name='炸板股池', dtype=str)
    df_zt_dtgc = pd.read_excel(file_path, sheet_name='跌停股池', dtype=str)

    return df_zt, df_zt_pvs, df_zt_strong, df_zt_sn, df_zt_zbgc, df_zt_dtgc


def load_industry_or_concept_stock(save_file, trade_date, industry_or_concept, sheet_name):
    file_path = save_file + '/' + str(trade_date) + '-' + str(industry_or_concept) + '.xlsx'
    df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)

    return df


def load_stocks(save_file, action_date, stock_code):
    # file_path = './' + save_file + '/' + str(action_date) + '-' + str(stock_code) + '.xlsx'
    file_path = save_file + '/' + str(action_date) + '-' + str(stock_code) + '.xlsx'
    daily = pd.read_excel(file_path, sheet_name='daily')
    weekly = pd.read_excel(file_path, sheet_name='weekly')
    monthly = pd.read_excel(file_path, sheet_name='monthly')

    return daily, weekly, monthly
