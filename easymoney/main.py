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

#接下来要实现获取个股数据的逻辑
#新建一个函数,命名为get_stock_detail，参数是stock_code

#获取股票详情数据：针对传进来的这只股票，请求个股详情接口，把需要的字段提取出来，做必要的数值换算，再把所属板块也取回来
#最后把结果封装成一个字典返回
def get_stock_detail(stock_code):
    #1、请求API拿响应
    #2、从响应体里把数据字段提取出来
    #3、把需要换算的值做单位换算（例如价格、涨跌幅、换手率都要除以100）
    #4、单独请求所属板块接口，拿到板块列表
    #5、把所有字段装进字典，返回给调用方



#接下来我们要解决的问题是：接口返回的响应结果不是标准的JSON，而是JSONP格式，外面包了一层函数调用，所以直接用response.json()会报错
#我们需要把外面的壳子去掉，只保留里面的JSON部分
#既然我们会用到的桑接口都是这种格式，那就写一个通用函数
#将响应文本转换为JSON对象
def convert_response_text_to_json(response_text):
    print(f"{response_text=}")#为了直观，先打印
    #接下来用正则表达式提取出JSON部分
    #先匹配开头的jQuery和后面的数字
    json_text = re.search(r"jQuery.*?\((\{.*?\})\)",response_text).group(1)
    #拿到JSON字符串后调用json.loads,把它转成Python的字典对象
    result_json = json.loads(json_text)
    #最后再打印一下，确认解析正确
    print(f"{result_json=}")
    #并return返回给调用方，这样一来，我们就把JSONP转换成立正常的JSON
    # 后面三个接口都可以直接用这个函数来处理响应结果
    return result_json

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
        #在函数get_stock_list里，我们已经拿到了接口的响应文本，接下来要做的，就是调用刚才写的convert_response_text_to_json
            #转换成正常的JSON对象
            #参数传入response.text,返回值就是一个python的字典，我们赋值给变量result_json
        result_json = convert_response_text_to_json(response.text)
            #然后我们从result_json里提取关键数据
            #最外层的data字段，包含了股票的总数和具体的股票列表，把它取出来赋值给变量data
        data = result_json["data"]
                #从data里先拿出来total，这个就是股票总数，复制给stock_cnt
        stock_cnt = data["total"]
                #再拿到diff，这个是股票的明细列表，赋值给stock_list
        stock_list = data["diff"]
            #接下来要把股票代码提取出来
                # 先新建一个空列表stock_code_list,用来存放股票代码
        stock_code_list = []
                #  然后写一个循环，循环变量命名为stock，逐个迭代stock_list
                #每个stock是一个字典，里面有一个字段f12，它对应的值就是股票代码
                #把它取出来，赋值给stock_code,再用append方法把它加到stock_code_list里
                #这样函数就能同时得到股票总数stock_cnt,以及这一页的所有股票代码列表stock_code_list
        for stock in stock_list:
            stock_code = stock["f12"]
            stock_code_list.append(stock_code)
            #提取完股票数量和股票代码之后我们需要把他们整理成一个统一的返回结果
            #这里新建一个字典stock_list_dict,里面放两个键值对
        stock_list_dict = {
            "stock_cnt" : stock_cnt,#第一个key是stock_cnt,对应的value就是刚才得到的股票总数stock_cnt
            "stock_code_list" : stock_code_list#第二个key是stock_code_list,对应的value是这一页的股票代码列表
        }
            #为了调试方便，再输出一下stock_list_dict
        print(f'{stock_list_dict=}')
            #最后把它作为函数返回值return出去
        return stock_list_dict


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
            #调用get_stock_list接口，并传入市场类型和页码1，也就是第一页的数据
            #函数会返回一个字典，赋值给stock_list_dict
        stock_list_dict = get_stock_list(market_type,1)
            #接着我们从里面取出stock_cnt的值，赋值给变量stock_cnt
        stock_cnt = stock_list_dict["stock_cnt"]
            #然后打印出来
        print(f"股票总数：{stock_cnt}")
            #运行后可以看到，输出的股票总数和页面上显示的一致，说明我们的股票列表接口调用成功了
        #2、根据股票总数实现分页循环
            #单页获取跑通之后，分页面获取也开始做，思路是根据总条数和每页条数，推导出要请求的页码，然后一页页去拉取并处理
            #我们先在这个函数内定义每页条数，这里按列表接口默认的每页20条计算
        page_size = 20
            #接下来需要一个循环变量，能依次取到0、20、40、60...直到最后一页之前的起始下标，最方便的就是用range(起始，结束，步长)
            #其中起始传0，结束传股票总数stock_cnt,步长传每页条数page_size,这样每页循环start刚好落在第一页开头
        for start in range(0,stock_cnt,page_size):
            #页码怎么算呢？页面从一开始计数，而start是从0开始的偏移量，所以我们用//，也就是向下取整的运算符
                #把start转成第几页的索引，再+1就是实际页码
            page_num = (start // page_size) + 1
            #接下来在每页的循环里，我们要去真正请求股票列表接口，获得这一页的股票代码
                #在循环体里，调用我们刚才写好的get_stock_list的函数，把market_type和page_num作为参数传进去
                #函数会返回一个字典，我们把它赋值给变量stock_list_dict
            stock_code_dict = get_stock_list(market_type, page_num)
                # 然后从这个字典里取出键stock_code_list对应的值，这个值就是一个股票代码的列表
            stock_code_list = stock_code_dict["stock_code_list"]
                #接着我们用for循环，从这个股票代码列表里，一个一个迭代出具体的股票代码，循环变量就命名为stock_code
                for stock_code in stock_code_list:



        #3、在分页循环中请求列表接口，获得股票列表
        #4、循环股票列表，获取个股详情数据
    except Exception as e:
        print(e)
        traceback.print_exc()


#最后补上主程序入口
#至于参数值，我们打开爬虫数据项文档，复制上证A股的市场类型值传入
if __name__ == '__main__':
    spider_stock_data("m:1+t:2+f:!2,m:1+t:23+f:!2")