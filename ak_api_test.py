from functools import lru_cache
import akshare as ak
import pandas as pd
import requests


stock_hk_tx_hist_df=stock_hk_hist(symbol="00700",start_date="20170301",end_date="20210913", adjust="qfq")

print(stock_hk_tx_hist_df)