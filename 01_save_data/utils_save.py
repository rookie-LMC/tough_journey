import akshare as ak
import pandas as pd


def export_stocks(save_file, stock_daily, stock_weekly, stock_monthly, action_date, stock_code):
    file_path = './' + save_file + '/' + str(action_date) + '-' + str(stock_code) + '.xlsx'
    print(file_path)
    # stock_date.to_excel(file_path, sheet_name=sheet_name)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        stock_daily.to_excel(writer, sheet_name='daily')
        stock_weekly.to_excel(writer, sheet_name='weekly')
        stock_monthly.to_excel(writer, sheet_name='monthly')


def export_hk_stocks(stock_daily, stock_weekly, stock_monthly, action_date, stock_code):
    file_path = './stock_info_hk' + '/' + str(action_date) + '-' + str(stock_code) + '.xlsx'
    print(file_path)
    # stock_date.to_excel(file_path, sheet_name=sheet_name)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        stock_daily.to_excel(writer, sheet_name='daily')
        stock_weekly.to_excel(writer, sheet_name='weekly')
        stock_monthly.to_excel(writer, sheet_name='monthly')


def load_stocks(save_file, action_date, stock_code):
    file_path = './' + save_file + '/' + str(action_date) + '-' + str(stock_code) + '.xlsx'
    daily = pd.read_excel(file_path, sheet_name='daily')
    weekly = pd.read_excel(file_path, sheet_name='weekly')
    monthly = pd.read_excel(file_path, sheet_name='monthly')

    return daily, weekly, monthly
