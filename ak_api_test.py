# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.font_manager import FontProperties
#
# # 指定字体文件路径（需根据实际情况修改）
# font_path = '/Users/limengchen03/SimHei.ttf'
# font = FontProperties(fname=font_path)
#
# # 生成示例数据
# data = np.random.rand(5, 5)
# labels = ['类别一', '类别二', '类别三', '类别四', '类别五']
#
# # 绘制热力图
# ax = sns.heatmap(data, annot=True, xticklabels=labels, yticklabels=labels)
#
# # 设置标题并指定字体
# ax.set_title('中文热力图示例', fontproperties=font)
# # 设置坐标轴标签并指定字体
# for tick in ax.get_xticklabels():
#     tick.set_fontproperties(font)
# for tick in ax.get_yticklabels():
#     tick.set_fontproperties(font)
#
# plt.show()



import pandas as pd
import plotly.graph_objects as go

# 示例数据
data = {
    '日期': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
    '收盘价': [100, 102, 101, 103, 100],
    '收盘价1': [100, 102, 101, 103, 100]

}
df = pd.DataFrame(data)
print(df)
# 将日期列转换为日期时间类型
df['日期'] = pd.to_datetime(df['日期'])

# 计算每日涨跌
df['涨跌'] = df['收盘价'].diff()
df['涨跌'] = df['涨跌'].fillna(0)

# 创建图形
fig = go.Figure()

# 添加涨跌柱状图
fig.add_trace(go.Bar(
    x=df['日期'],
    y=df['涨跌'],
    marker_color=['green' if x >= 0 else 'red' for x in df['涨跌']]
))

# 更新布局
fig.update_layout(
    title='每日涨跌情况',
    xaxis_title='日期',
    yaxis_title='涨跌'
)

# 显示图形
fig.show()