import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

data = pd.read_csv("疫情大数据分析\\爬虫数据\\全国数据.csv")

# 数据录入——请在这里修改或补充每日病例数，数据太多时用"\"表示换行
confirmedCount = data.loc[0:100, "确诊总数"].to_list()

days = len(confirmedCount)  # 自动计算上面输入的数据所对应的天数
xdata = [i + 1 for i in range(days)]  # 横坐标数据，以第几天表示
ydata = confirmedCount  # 纵坐标数据，表示每天对应的病例数
plt.scatter(xdata, ydata, label='data')  # 把输入的数据用散点图列印出来


# S型曲线函数公式定义
def func(x, k, a, b):
    return k / (1 + (k / b - 1) * np.exp(-a * x))


# 非线性最小二乘法拟合
popt, pcov = curve_fit(func, xdata, ydata, method='dogbox', \
                        bounds=([1000., 0.01, 10.],[10000000., 1.0, 1000.]))
k = popt[0]
a = popt[1]
b = popt[2]

# 计算拟合数据后的数据
延长天数 = 7  # 需要预测的天数
x = np.linspace(0, len(xdata) + 延长天数)  # 横坐标取值
y = func(x, *popt)  # 纵坐标计算值

# 作图
plt.plot(x, y, color='r', label='fit')  # 对拟合函数作图
plt.xlabel('Day')  # 打印横坐标标签
plt.ylabel('Number of Cases')  # 打印纵坐标标签
plt.title('A Rough Simulation and Prediction')  # 打印图表名称
plt.legend(loc='best')  # 打印图例说明
# plt.show()  # 正式输出图表
plt.savefig("疫情大数据分析\\图\\预测曲线.png")
