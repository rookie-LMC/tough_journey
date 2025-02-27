import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.table import Table
from matplotlib.font_manager import FontProperties

font_path = '/Users/limengchen03/SimHei.ttf'
font = FontProperties(fname=font_path)
# 模拟数据
data = {
    'rank': [1, 2, 3, 4, 5, 6, 7, 8],
    '01-27': [('银行', '+1.49%'), ('燃气', '+0.95%'), ('煤炭行业', '+0.94%'), ('农药兽药', '+0.88%'),
              ('电力行业', '+0.81%'), ('钢铁行业', '+0.81%'), ('医药商业', '+0.78%'), ('化肥行业', '+0.74%')],
    '01-24': [('互联网服务', '+4.12%'), ('软件开发', '+4.02%'), ('文化传媒', '+3.03%'), ('消费电子', '+2.92%'),
              ('计算机设备', '+2.61%'), ('游戏', '+2.41%'), ('教育', '+2.33%'), ('通信服务', '+2.18%')],
    '01-23': [('保险', '+5.14%'), ('银行', '-2.43%'), ('教育', '+1.70%'), ('多元金融', '+1.53%'),
              ('文化传媒', '+0.89%'), ('证券', '+0.74%'), ('铁路公路', '+0.66%'), ('物流行业', '+0.46%')]
}

df = pd.DataFrame(data)
print('数据长度: ', len(df))
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
for i in range(len(df)):
    table.add_cell(i + 1, 0, 1, 1, text=str(df['rank'][i]), loc='center', facecolor='none')
    for j in range(1, len(col_labels)):
        industry, change = df[col_labels[j]][i]
        cell = table.add_cell(i + 1, j, 1, 1, text=f'{industry}\n{change}', loc='center', facecolor='none')

        # 设置背景颜色
        color = 'red' if change.startswith('+') else 'green'
        cell.set_facecolor(color)
        cell.get_text().set_fontproperties(font)

# 将表格添加到子图
ax.add_table(table)

# 显示图形
plt.show()
