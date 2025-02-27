import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.table import Table
from matplotlib.font_manager import FontProperties
import akshare as ak
import datetime as dt

# 中文显示
font_path = '/Users/limengchen03/SimHei.ttf'
font = FontProperties(fname=font_path)

# # 模拟数据
# data = {
#     'rank': [1, 2, 3, 4, 5, 6, 7, 8],
#     '01-27': [('银行', '+1.49%'), ('燃气', '+0.95%'), ('煤炭行业', '+0.94%'), ('农药兽药', '+0.88%'),
#               ('电力行业', '+0.81%'), ('钢铁行业', '+0.81%'), ('医药商业', '+0.78%'), ('化肥行业', '+0.74%')],
#     '01-24': [('互联网服务', '+4.12%'), ('软件开发', '+4.02%'), ('文化传媒', '+3.03%'), ('消费电子', '+2.92%'),
#               ('计算机设备', '+2.61%'), ('游戏', '+2.41%'), ('教育', '+2.33%'), ('通信服务', '+2.18%')],
#     '01-23': [('保险', '+5.14%'), ('银行', '-2.43%'), ('教育', '+1.70%'), ('多元金融', '+1.53%'),
#               ('文化传媒', '+0.89%'), ('证券', '+0.74%'), ('铁路公路', '+0.66%'), ('物流行业', '+0.46%')]
# }
# df = pd.DataFrame(data)

# 观察数据
# stocks_code = [['06680', '金力永磁', 1], ['02727', '上海电气', 2], ['09868', '小鹏汽车-W', 2], ['01070', 'TCL电子', 1]]

stocks_code = [['01675', '亚信科技'],
               ['09988', '阿里巴巴-W'],
               ['00241', '阿里健康'],
               ['03896', '金山云'],
               ['06181', '老铺黄金'],
               ['01385', '上海复旦'],
               ['01024', '快手-W'],
               ['01347', '华虹半导体'],
               ['09880', '优必选'],
               ['01833', '平安好医生'],
               ['02498', '速腾聚创'],
               ['09992', '泡泡玛特'],
               ['06680', '金力永磁'],
               ['06869', '长飞光纤光缆'],
               ['00909', '明源云'],
               ['00763', '中兴通讯'],
               ['00981', '中芯国际'],
               ['00268', '金蝶国际'],
               ['00285', '比亚迪电子'],
               ['01177', '中国生物制药'],
               ['01316', '耐世特'],
               ['01357', '美图公司'],
               ['02465', '龙蟠科技'],
               ['01810', '小米集团-W'],
               ['03888', '金山软件'],
               ['02018', '瑞声科技'],
               ['02252', '微创机器人-B'],
               ['01274', '知行汽车科技'],
               ['02382', '舜宇光学科技'],
               ['02015', '理想汽车-W'],
               ['09890', '中旭未来'],
               ['00013', '和黄医药'],
               ['09989', '海普瑞'],
               ['01070', 'TCL电子'],
               ['06078', '海吉亚医疗'],
               ['01119', '创梦天地'],
               ['02228', '晶泰控股-P'],
               ['06660', '艾美疫苗'],
               ['03933', '联邦制药'],
               ['03396', '联想控股'],
               ['01478', '丘钛科技'],
               ['02268', '药明合联'],
               ['02487', '科笛-B'],
               ['02192', '医脉通'],
               ['02556', '迈富时']]

start_date = '20250105'
ob_N_days = 15
debug_num = 20000
sleep_time = 0.4

# 数据初始化
cycle_data = {}
cycle_data['rank'] = [i + 1 for i in range(len(stocks_code))]
hk_df = ak.stock_hk_hist(stocks_code[0][0], adjust="qfq", period="daily", start_date=start_date)
for j in range(ob_N_days):
    cycle_data[str(hk_df[['日期', '涨跌幅']].iloc[-j - 1, 0])] = []
print(cycle_data)

for i in range(min(len(stocks_code), debug_num)):
    try:
        print('**** load K line : ', stocks_code[i][0])
        hk_df = ak.stock_hk_hist(stocks_code[i][0], adjust="qfq", period="daily",
                                 start_date=start_date)
        for j in range(ob_N_days):
            tmp = [stocks_code[i][1], hk_df[['日期', '涨跌幅']].iloc[-j - 1, 1]]
            cycle_data[str(hk_df[['日期', '涨跌幅']].iloc[-j - 1, 0])].append(tmp)
        time.sleep(sleep_time)
    except:
        print('**** has no K line: ', stocks_code[i][0])

for j in range(ob_N_days):
    cycle_data[str(hk_df[['日期', '涨跌幅']].iloc[-j - 1, 0])].sort(key=lambda x: x[1], reverse=True)
print(cycle_data)
df = pd.DataFrame(cycle_data)

print('数据长度: ', len(df), df)
# 创建图形和子图
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis('off')  # 关闭坐标轴

# 创建表格
table = Table(ax, bbox=[0, 0, 1, 1])

# 添加表头
col_labels = df.columns
print('数据表头: ', col_labels)
for j in range(len(col_labels)):
    table.add_cell(0, j, 1, 1, text=col_labels[j], loc='center', facecolor='lightgray')

# 添加数据行
min_font_size, max_font_size = 6, 20
for i in range(len(df)):
    table.add_cell(i + 1, 0, 1, 1, text=str(df['rank'][i]), loc='center', facecolor='none')
    for j in range(1, len(col_labels)):
        industry, change = df[col_labels[j]][i]
        text = f'{industry}\n{change}'
        cell = table.add_cell(i + 1, j, 1, 1, text=text, loc='center', facecolor='none')

        # 简单的根据文本长度调整字体大小
        text = str(industry)
        text_length = len(text)
        font_size = max_font_size - text_length * 2
        # 确保字体大小在最小和最大范围之间
        font_size = max(min_font_size, min(font_size, max_font_size))
        cell.get_text().set_fontsize(font_size)

        # 设置背景颜色
        color = 'red' if change > 0 else 'green'
        cell.set_facecolor(color)
        cell.get_text().set_fontproperties(font)

# 将表格添加到子图
ax.add_table(table)

# 显示图形
plt.show()
