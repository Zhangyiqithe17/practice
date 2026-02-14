import requests
#用来发起HTTP请求
import json
#用来把接口返回的JSON文本解析成python数据结构
import re
#在处理JSONP响应，用正则把外层的回调函数壳子去掉
import datetime
#对时间戳进行转换
import time
#备用，后面做分页请求或限速时，可以适当sleep
import traceback
#用来打印完整堆栈，定位问题非常直观

#接着写函数spider_stock_data,它接收一个market_type参数，这个参数就是我们前面在调试股票列表API时确认过的fs的取值，用来指定交易市场类型
#这样写的目的是把目标市场的选择权交给调用方，后面改市场只需要修改传入的参数即可
#函数体先用try except把整体流程包起来,except里我们调用print(e)和traceback.print_exc()，前者可以让我们快速看到报错信息，后者能把调用链完整展示出来
#在函数体里，先不要着急写具体实现，而是用注释把整个流程规划清楚
def spider_stock_data(market_type):
    try:
        #1、先请求列表接口，获得股票总数
        #2、根据股票总数实现分页循环
        #3、在分页循环中请求列表接口，获得股票列表
        #4、循环股票列表，获取个股详情数据
    except Exception as e:
        print(e)
        traceback.print_exc()


#最后补上主程序入口
#至于参数值，我们打开爬虫数据项文档，复制上证A股的市场类型值传入
if __name__ == '__main__':
    spider_stock_data("m:1+t:2+f:!2,m:1+t:23+f:!2")