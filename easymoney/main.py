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

#接下来实现获取股票列表的逻辑
#新建函数get_stock_list，它接收两个参数market_type和page_num
#market_type用来制定交易市场类型，page_num表示页码
#函数用于获取股票列表，返回字典数据
def get_stock_list(market_type,page_num):
    print(f"请求页码：{page_num=}")
    #1、请求股票列表API把接口数据取回
        # 在请求API的部分，我们可以直接利用Postman，之前保存的股票列表API，生成代码
        #粘贴后我们要做几处修改：
            #1、删除多余import，只保留函数体
            #2、把URL改成f-字符串：具体来说，我们找到URL里的fs参数，用传进来的变量market_type替换，pn参数用page_num替换
            #3、在函数开头打印页码，方便调试时知道当前请求是第几页
            #4、用try except包裹请求逻辑，except里用raise抛出异常
            #5、在try里调用response.raise_for_status(),请求失败会自动抛出异常，不需要我们自己写状态码判断
    url = f"https://push2.eastmoney.com/api/qt/clist/get?np=1&fltt=1&invt=2&cb=jQuery371005505359543172528_1771055558285&fs={market_type}&fields=f12,f13,f14,f1,f2,f4,f3,f152,f5,f6,f7,f15,f18,f16,f17,f10,f8,f9,f23&fid=f3&pn={page_num}&pz=20&po=1&dect=1&ut=fa5fd1943c7b386f172d6893dbfba10b&wbp2u=|0|0|0|web&_=1771055558287"

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
    except Exception as e:
        traceback.print_exc()
        raise Exception(f"获取股票列表失败：e：{e}")

    #2、从返回结果里提取出股票总数和股票列表
    #3、把他们放进一个字典里，作为函数返回值
    #这样我们在主流程里，只要调用一次函数，就能拿到一整页的股票数据


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