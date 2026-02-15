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
        #切换到Postman,打开个股详情API的请求，复制生成的示例代码，复制到此处
        #然后把URL写成f-字符串，具体来说，我们需要把股票代码作为变量，动态拼进secid
    url = f"https://push2.eastmoney.com/api/qt/stock/get?invt=2&fltt=1&cb=jQuery123&fields=f58%2Cf734%2Cf107%2Cf57%2Cf43%2Cf59%2Cf169%2Cf301%2Cf60%2Cf170%2Cf152%2Cf177%2Cf111%2Cf46%2Cf44%2Cf45%2Cf47%2Cf260%2Cf48%2Cf261%2Cf279%2Cf277%2Cf278%2Cf288%2Cf19%2Cf17%2Cf531%2Cf15%2Cf13%2Cf11%2Cf20%2Cf18%2Cf16%2Cf14%2Cf12%2Cf39%2Cf37%2Cf35%2Cf33%2Cf31%2Cf40%2Cf38%2Cf36%2Cf34%2Cf32%2Cf211%2Cf212%2Cf213%2Cf214%2Cf215%2Cf210%2Cf209%2Cf208%2Cf207%2Cf206%2Cf161%2Cf49%2Cf171%2Cf50%2Cf86%2Cf84%2Cf85%2Cf168%2Cf108%2Cf116%2Cf167%2Cf164%2Cf162%2Cf163%2Cf92%2Cf71%2Cf117%2Cf292%2Cf51%2Cf52%2Cf191%2Cf192%2Cf262%2Cf294%2Cf181%2Cf295%2Cf269%2Cf270%2Cf256%2Cf257%2Cf285%2Cf286%2Cf748%2Cf747&secid=1.{stock_code}&ut=fa5fd1943c7b386f172d6893dbfba10b&wbp2u=%7C0%7C0%7C0%7Cweb&dect=1&_=1771054408829"

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
    }
        #然后把请求和解析包进try...except,并在try下方调用response.raise_for_status(),拦截非200的HTTP错误
        #以及在except的下方出现任何异常时，raise一个带上下文的异常，表明获取个股详情失败，把错误抛回给调用方
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        #把response.text丢给我们前面写好的convert_response_text_to_json，把JSONP转成标准的JSON，返回值先放在result_json
        result_json = convert_response_text_to_json(response.text)
        #下一步就可以做字段提取与数值换算了
        # 2、从响应体里把数据字段提取出来
            # 接下来我们要从result_json中提取需要的字段，把它们填充到字典数据中
            # 为了方便操作，先打开txt文档，把个股详情接口响应结果里的data部分，复制粘贴到代码里，这样就能对照逐个字段提取
            # "f43": 9498, // 最新股价，除以100等于浮点数
            # "f48": 1228447273.0, // 交易日成交额，记录原始数据
            # "f57": "688147", // 股票代码
            # "f58": "微导纳米", // 股票名称
            # "f86": 1770970295, // 数据更新时间
            # "f116": 43800718739.340007, // 总市值，记录原始数据
            # "f117": 43800718739.340007, // 流通市值，记录原始数据
            # "f162": 13220, // 动态市盈率，除以100等于浮点数
            # "f163": 19320, // 静态市盈率，除以100等于浮点数
            # "f164": 13500, // 滚动市盈率，除以100等于浮点数
            # "f167": 1516, // 市净率，除以100等于浮点数
            # "f168": 293, // 交易日换手率，除以100等于浮点数
            # "f170": 1457, // 交易日涨跌幅，除以100等于浮点数
            # "f288": 0, // 是否盈利，0表示是，1表示否
            #首先从其中提取出data字段,因为所有数值信息都存储在data里面
        data = result_json["data"]
            #接下来从data依次提取我们需要的字段，并赋值给对应的变量
        price = data["f43"]
        if "-" in str(price):
            print(f"股票已退市，跳过爬取，股票代码：{stock_code}")
            return None
        trading_value = data["f48"]
        stock_code = data["f57"]
        stock_name = data["f58"]
        update_time = data["f86"]
        total_market_cap = data["f116"]
        circulating_market_cap = data["f117"]
        dynamic_pe_ratio = data["f162"]
        static_pe_ratio = data["f163"]
        rolling_pe_ratio = data["f164"]
        pb_ratio = data["f167"]
        turnover_rate = data["f168"]
        price_change_percent = data["f170"]
        is_profitable = data["f288"]
            #在赋值完成后，还要特别注意一个问题，有些个股可能已经退市，没有价格数据
            #退市股票在接口里f43字段的值不是数字，而是“-”这样的字符串，如果我们直接用来做数值计算，就会报错
            #所以我们需要先做一个判断：如果price被转换为字符串之后，里面包含符号"-",那么说明这只股票已经退市
                #直接跳过，不做处理，这时print输出一行提示
        # 3、把需要换算的值做单位换算（例如价格、涨跌幅、换手率都要除以100）
            #接口里有很多数值字段和页面上展示的不一样，比如价格涨跌幅换手率等，需要先除以100才能对应到页面上的小数值
            #所以思路是：先把原始值强制转成int，再除以对应的比例，最后转成float写到原变量里
        price = float(int(price) / 100)
        price_change_percent = float(int(price_change_percent) / 100)
        turnover_rate = float(int(turnover_rate) / 100)
        dynamic_pe_ratio = float(int(dynamic_pe_ratio) / 100)
        static_pe_ratio = float(int(static_pe_ratio) / 100)
        rolling_pe_ratio = float(int(rolling_pe_ratio) / 100)
        pb_ratio = float(int(pb_ratio) / 100)
            #是否盈利是布尔值，但在接口里要用0/1表示，可以把它映射成人类可读的“是/否”
        is_profitable = "是" if is_profitable == 0 else "否"
            #更新时间是时间戳，我们转换成datetime对象，方便后续入库与展示
        update_time = datetime.datetime.fromtimestamp(update_time)
            #最后把所有字段名和对应的值打印出来，方便确认效果
        print(f"股票代码:{stock_code},股票名称:{stock_name},更新时间:{update_time},最新价:{price}\n"
              f"交易日涨跌幅:{price_change_percent},交易日成交额:{trading_value},换手率:{turnover_rate}"
              f"总市值:{total_market_cap},流通市值:{circulating_market_cap},是否盈利:{is_profitable}"
              f"动态市盈率:{dynamic_pe_ratio},静态市盈率:{static_pe_ratio},滚动市盈率:{rolling_pe_ratio}")
        # 4、单独请求所属板块接口，拿到板块列表
        # 5、把所有字段装进字典，返回给调用方

    except Exception as e:
        raise Exception(f"获取个股详情失败：e：{e}")






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
    # print(f"{result_json=}")
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
                # for stock_code in stock_code_list:
                #为了对get_stock_detail函数进行验证，我们先注释掉for循环，注释main里面对spider_stock_data的调用
                    #然后调用get_stock_detail，传入一个股票代码，运行看看效果



        #3、在分页循环中请求列表接口，获得股票列表
        #4、循环股票列表，获取个股详情数据
    except Exception as e:
        print(e)
        traceback.print_exc()


#最后补上主程序入口
#至于参数值，我们打开爬虫数据项文档，复制上证A股的市场类型值传入
if __name__ == '__main__':
    # spider_stock_data("m:1+t:2+f:!2,m:1+t:23+f:!2")
    get_stock_detail(601929)