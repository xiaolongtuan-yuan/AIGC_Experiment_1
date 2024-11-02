# -*- coding: utf-8 -*-
"""
@Time ： 2024/5/20 15:37
@Auth ： xiaolongtuan
@File ：draw_chart.py
"""
import os.path
import threading
import matplotlib.font_manager as fm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator
from scipy.interpolate import CubicSpline

font_path = "resources/Songti.ttc"
lock = threading.Lock()


def csv_Line_chart(title, csv_file):
    df = pd.read_csv(csv_file)
    if len(df.columns) > 2:
        print("csv file has more than 2 columns, use the first column as x_lable, the second column as y_lable")
    plot_Line_chart(title, df.columns[0], df.columns[1], df[df.columns[0]], df[df.columns[1]],
                    os.path.join("images", title + ".jpg"))
    return os.path.join("images", title + ".jpg")


def csv_pie_chart(title, csv_file):
    df = pd.read_csv(csv_file)
    if len(df.columns) > 2:
        print("csv file has more than 2 columns, use the first column as label, the second column as size")
    draw_pie_chart(title, list(df[df.columns[1]]), list(df[df.columns[0]]), os.path.join("images", title + ".jpg"))
    return os.path.join("images", title + ".jpg")


def plot_Line_chart(title, x_lable, y_lable, x=['标签一', '标签二', '标签三', '标签四'], y=[10, 15, 7, 10], path=None):
    with lock:
        prop = fm.FontProperties(fname=font_path)
        plt.figure(figsize=(15, 6))  # 设置图表大小
        plt.plot(x, y, marker='o', mfc="white")  # 绘制折线图，点标记为'o'

        # # 在每个数据点上添加数值标签
        # for i, value in enumerate(y):
        #     plt.text(x[i], value + 0.5, '{:.2f}'.format(value), ha='center', fontproperties=prop)  # 偏移0.5以避免与点重叠

        # 设置图表标题和坐标轴标签
        plt.title(title, fontproperties=prop, fontsize=16)
        plt.xlabel(x_lable, fontproperties=prop)
        plt.ylabel(y_lable, fontproperties=prop)
        # 设置x轴和y轴刻度标签的字体
        max_x_label = 15
        if len(x) <= max_x_label:
            plt.xticks(ticks=range(len(x)), labels=x, fontproperties=prop, rotation=45)
        else:
            plt.xticks(fontproperties=prop, rotation=45)
        plt.yticks(fontproperties=prop)

        ax = plt.gca()

        # 优化网格线条，隐藏边框
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(ls="--", lw=0.5, color="#4E616C")
        if len(x) > max_x_label:
            ax.xaxis.set_major_locator(MaxNLocator(max_x_label, prune=None))  # 最多显示15个刻度

        plt.grid(True)  # 显示网格
        plt.tight_layout()
        if path:
            plt.savefig(path)
            # plt.show()
        plt.clf()


def draw_pie_chart(title, data, label, path=None):
    with lock:
        plt.switch_backend('Agg')
        font_size = max(10, 15 - len(label) * 0.5)
        title_font = fm.FontProperties(fname=font_path, size=20)  # 更大的字体大小用于标题
        legend_font = fm.FontProperties(fname=font_path, size=font_size)  # 更小的字体大小用于图例
        plt.figure(figsize=(8, 6))

        sizes = data

        # 设置颜色（可选）
        colors = [
            '#ff9999',  # 淡粉色
            '#66b3ff',  # 浅蓝色
            '#99ff99',  # 淡绿色
            '#ffcc99',  # 浅橙色
            '#c2c2f0',  # 淡紫色
            '#ffb3e6',  # 浅玫瑰色
            '#c4e17f',  # 浅黄绿色
            '#76d7c4',  # 浅青色
            '#f7b7a3',  # 浅珊瑚色
            '#f8c471'  # 浅金色
        ]
        explode = [0.1 if i == label.index(max(label, key=len)) else 0 for i in range(len(label))]
        plt.pie(sizes, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        plt.title(title, fontproperties=title_font, loc='center')
        plt.legend(label, loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1), prop=legend_font)  # 把图例放在图外
        plt.tight_layout()
        if path:
            plt.savefig(path)
        plt.clf()


if __name__ == '__main__':
    # csv_Line_chart("3月营业额", "images/march_revenue.csv")
    csv_pie_chart("3月各房型销售情况", "files/march_room_revenue.csv")
