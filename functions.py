import tkinter as tk
from numpy import polyfit


class Stock:
    def __init__(self, code, start_time=20190101, end_time=20200527):  # 默认从2019年1月开始，本地数据大部分从2015年开始，但有些股票会晚一些
        self.code = code
        self.start_time = start_time
        self.end_time = end_time

    def stock_name(self):
        data_unwashed = open(f'Stock/SH#{self.code}.txt', 'r')
        first_line = data_unwashed.readline()
        first_line = first_line.split()
        return first_line[0] +' ' + first_line[1]

    # 因为如果需要获取实时的沪指数据的话需要import tushare的API，导出的数据是array，这样会用到pandas数据分析模块，
    # 可能不符合大作业的要求，所以就用了本地数据
    def get_stock_data(self):
        data_unwashed = open(f'Stock/SH#{self.code}.txt', 'r')  # 原先的本地数据是纯文本形式的，所以这里用wash函数把原数据转为list
        data = wash(data_unwashed, self.start_time, self.end_time)
        return data

    def show_daily_increasing_rate(self):  # 因为数据从输入的那一天开始，所以第一天的涨幅无法计算，所以涨幅从输入的开始日期后一天开始
        data = self.get_stock_data()
        daily_rate = []
        for i in range(1, len(data)):
            rate = round((float(data[i][4]) - float(data[i - 1][4])) / float(data[i - 1][4]), 6)  # 涨幅保留了六位小数
            daily_rate.append(rate)
        return daily_rate

    def draw_k_chart_latest_x_days(self, x=30):  # 定义画给定时间段最近x天k线图的函数，默认为30天
        stock_name = self.stock_name()
        root = tk.Tk()
        c = tk.Canvas(root, width=700, height=600, bg='white')
        c.create_text(350, 10, text=stock_name)

        data = self.get_stock_data()
        data_x_days = data[-x:]
        max_in_one_day = []
        min_in_one_day = []
        for i in range(1, x + 1):
            max_day = float(data_x_days[i-1][2])
            max_in_one_day.append(max_day)
            min_day = float(data_x_days[i-1][3])
            min_in_one_day.append(min_day)
        max_total = max(max_in_one_day)        # 求出x天内股价的最高点
        min_total = min(min_in_one_day)        # 求出x天内股价的最低点
        c.create_text(25, 20, text=str(max_total))
        c.create_text(25, 440, text=str(min_total))

        for i in range(1, x + 1):
            if float(data_x_days[i-1][1]) > float(data_x_days[i-1][4]):
                color = 'green'
            else:
                color = 'red'

            if self.code == '999999':    # 如果是沪指，交易量过大，会超出canvas，所以进行处理
                a = float(data_x_days[i - 1][5])/15000000
            else:
                a = float(data_x_days[i - 1][5])/500000
            c.create_line(300/x+(700-300/x)/x*0.35+(700-300/x)/x*(i-1),
                          440 - 420*(float(data_x_days[i-1][2])-min_total)/(max_total - min_total),
                          300/x+(700-300/x)/x*0.35+(700-300/x)/x*(i-1),
                          440 - 420*(float(data_x_days[i-1][3])-min_total)/(max_total - min_total),
                          fill=color)   # 画出当日最高价、最低价
            c.create_rectangle(300/x+(700-300/x)/x*(i-1), 600 - a,
                               300/x+(700-300/x)/x*0.8+(700-300/x)/x*(i-1), 600,
                               outline=color, fill=color)    # 画出交易量的图形
            c.create_rectangle(300/x+(700-300/x)/x*(i-1), 440 - 420*(float(data_x_days[i-1][1])-min_total)/(max_total - min_total),
                               300/x+(700-300/x)/x*0.8+(700-300/x)/x*(i-1), 440 - 420*(float(data_x_days[i-1][4])-min_total)/(max_total - min_total),
                               outline=color, fill=color)   # 画出开盘价、收盘价图形
        c.pack()

    def calculate_beta(self):    # 定义一个计算指定股票beta值的函数，其中计算beta要用到线性回归，所以这里调用了numpy里的polyfit函数简化计算
        increasing_rate = self.show_daily_increasing_rate()
        shanghai_index = Stock('999999', self.start_time, self.end_time)    # beta值的计算依赖于大盘指数，所以这里调用沪指
        shanghai_index_rate = shanghai_index.show_daily_increasing_rate()
        beta = round(float(polyfit(increasing_rate, shanghai_index_rate, deg=1)[0]), 5)  # 最后的beta值保留5位小数
        return beta


def wash(data_unwashed, start_time, end_time):    # 本地的stock数据是纯文本形式，这里定义wash函数转换成list
    data = data_unwashed.readlines()
    data_washed1 =[]
    for lines in data:
        line = lines.split()
        data_washed1.append(line)
    data_washed = []
    for i in range(2, len(data_washed1) - 1):
        if start_time <= int(data_washed1[i][0]) <= end_time:
            data_washed.append(data_washed1[i])
    return data_washed


