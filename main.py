# import requests
from curl_cffi import requests
#导入python内置time，后续用来增加请求之间的时间间隔
import time
from lxml import etree

#提取岗位所在地
def get_job_region(job_item):
    #因为xpath的返回值是一个文本列表，所以还要用[0]取出里面第一个元素
    region_text = job_item.xpath(".//div[@class = 'jobinfo__other-info-item'][1]/span[1]/text()")[0]
    print(f'region_text = {region_text}')

#解析搜索页面
def parse_search_page(page_url,page_num):#两个参数，一个是页面地址，一个表示当前搜索的是第几页
    #把请求和解析的逻辑集中到函数里面
    try:
        # 接下来再验证一下详情页数据，是否也是可以直接通过发送请求获取到的
        # 切换回浏览器，复制任何一个岗位详情页的URL，把他赋值给一个新变量url_detail,并替换掉requests.get里的参数
        # url_detail = 'https://www.zhaopin.com/jobdetail/CC000544460J40776127616.htm?refcode=4019&srccode=401903&preactionid=ec7bcbcd-def9-439f-8587-81f26684e0aa'
        response = requests.get(url, headers=headers)
        # response = requests.get(url_detail, headers=headers)
        #运行程序后，在输出的HTML再次搜索，从结果可以看到，岗位详情页也可以用requests结合Xpath的方式抓取数据
        response.raise_for_status()
        # print(response.text)
        #这就是网页服务器返回的HTML代码

        #1。将HTML内容转换为文档对象
        tree = etree.HTML(response.text)
        print(f'正在解析第{page_num}页')

        #2。提取岗位列表
        job_item_list = tree.xpath(".//div[@class='joblist-box__iteminfo']")
        print(f'找到了{len(job_item_list)}个岗位')
        for job_item in job_item_list:
            get_job_region(job_item)
            #3。提取岗位所在地
            #4。提取详情页URL
            #5。解析详情页
        #6。实现分页逻辑

    except Exception as e:
        print(f'解析搜索页面异常:{e}')

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
    }
    url = 'https://www.zhaopin.com/sou/jl765/kwE8M8CQO/p1'

    parse_search_page(url,1)

    #如果在运行结果里看到了完整的HTML，那么就可以进行下一步了
    #但是像现在这个代码的运行结果一样：响应的结果里只有一点点HTML，而且还可以看到像TCaptcha.js这样的关键词，就基本可以判断：
    #我们的情趣被网站的风控识别成了不可信，于是被重定向到了验证码页面
    #所以我们要把请求伪装得更像真是浏览器，看看能否绕过这类基础校验

    #实践里一个成本很低的尝试是改用curl_cffi提供的requests兼容接口，它很多时候能比标准requests更容易通过初级风控
    #那么第一步是安装依赖，在pycharm终端里运行安装命令pip install curl_cffi
    #等安装完成后回到代码，把原来的导入语句替换掉，不再import requests，而是用from curl_cffi import requests
    #再次运行，就能在返回的HTML里看到完整的页面结构了

    #接着在终端里按快捷键Ctrl + F，打开搜索框，输入关键字“万”，用上下箭头切换查找结果，说明这些内容确实包含在HTML代码里
    #接下来就可以用XPath或BS4解析列表页

    #正式写代码之前，还可以做一个准备工作：就是把每个要爬取的数据项在网页上对应的位置找出来，记录到文档里
    #这样到时候写XPath的时候，就不用在浏览器和代码编辑器上切换了