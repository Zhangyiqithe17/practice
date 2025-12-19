# import requests
from curl_cffi import requests
#导入python内置time，后续用来增加请求之间的时间间隔
import time
import re

from dateutil.relativedelta import relativedelta
from lxml import etree
from datetime import date,datetime



#提取岗位说明
def get_job_desc(tree):
    job_desc_text = tree.xpath('//div[@class="describtion__detail-content"]/text()')
    print(f"{job_desc_text=}")
    return job_desc_text

#提取岗位技能标签
def get_job_skills(tree):
    job_skills =  tree.xpath("//span[@class = 'describtion__skills-item']/text()")
    # print(f'{job_skills=}')
    return job_skills

#提取li标签中的文本
def get_summary_li_text(li_elements,index):
    if len(li_elements)  > index:
        #如果条件成立，说明这个索引对应的li确实存在
        #如果条件不成立，说明对应的数据项在当前岗位页面可能有缺失，直接return""
        #这样即使缺少某个字段，爬虫也能正常运行，而不是报错中断
        li_element = li_elements[index]
        text_list = li_element.xpath('.//text()')
        #拿到text_list后，还要确认它确实有内容，如果列表长度大于0，说明至少有一个文本节点
        if len(text_list) > 0:
            return text_list[0]
        else:
            return ''
    else:
        return ''


#提取要求的工作经验、要求的学历、雇佣方式和招聘人数，返回字典
def get_job_summary_info(tree):
    #但是针对各个岗位信息，可能不是所有li标签都存在，为了避免索引越界引发异常，可以先写一个工具函数专门做文本提取
    #如果这个索引的li不存在，直接返回空字符串，如果存在，就从中取出文本
    li_elements = tree.xpath("//ul[@class = 'summary-plane__info']/li")
    #接下来已经拿到了所有li标签，接下来就是取值
    #因为这些字段是按照固定顺序排列的，可以用索引值来区分他们
    #索引1对应工作经验 索引2对应学历 索引3对应雇佣方式 索引4对应招聘人数
    req_work_experience = get_summary_li_text(li_elements,1)
    req_education = get_summary_li_text(li_elements, 2)
    employment_type = get_summary_li_text(li_elements, 3)
    recruit_count_text = get_summary_li_text(li_elements, 4)
    recruit_count_match = re.search(r'\d+', recruit_count_text)
    recruit_count = recruit_count_match.group() if recruit_count_match else ''

    summary_info_dict = {
        "req_work_experience":req_work_experience,
        "req_education":req_education,
        "employment_type":employment_type,
        "recruit_count":recruit_count
    }
    # print(f"{summary_info_dict=}")
    return summary_info_dict

#提取薪酬范围 返回值为字典，包括薪酬福利、最低工资和最高工资
def get_job_salary(tree):
    job_salary_text= tree.xpath('//span[@class = "summary-plane__salary"]/text()')[0]
    print(f"{job_salary_text=}")
    if "面议" in job_salary_text:
        salary_dict = {
            "salary_type" : "面议",#薪酬计算方式
            "salary_extra" : "",#附加福利
            "salary_min": 0,
            "salary_max": 0,
        }
        print(f"{salary_dict=}")
        return salary_dict
    #如果不是面议，我们就需要把它规整为可计算的数字
    #包括要对以万为单位的写法和以元为单位的写法进行统一，并且吧类似13薪的附加福利拆分开进行保存
    salary_type = "月"
    salary_range = job_salary_text
    if "天" in job_salary_text:
        salary_type = "天"
        salary_range = salary_range.replace("/天","")

    #判断是否包含附件的福利薪酬
    salary_split_list = salary_range.split("·")
    salary_range = salary_split_list[0]
    salary_extra = ''
    if len(salary_split_list) > 1:
        salary_extra = salary_split_list[1]

    #将薪酬区间转换为纯数字
    salary_format = "元"
    if "万" in salary_range:
        salary_format = "万"
    #然后把里面的万和元都去掉
    salary_range = salary_range.replace("万","").replace("元","")
    salary_range_list = salary_range.split("-")
    salary_min = float(salary_range_list[0])
    salary_max = float(salary_range_list[1])
    #单位转换
    if salary_format == "万":
        salary_min = salary_min * 10000
        salary_max = salary_max * 10000

    salary_dict = {
        "salary_type": salary_type,  # 薪酬计算方式
        "salary_extra": salary_extra,  # 附加福利
        "salary_min": int(salary_min),
        "salary_max": int(salary_max),
    }
    # print(f"{salary_dict=}")
    return salary_dict



#提取岗位名称
def get_job_name(tree):
    job_name = tree.xpath('//h3[@class = "summary-plane__title"]/text()')[0]
    print(f"{job_name=}")
    return job_name

#提取岗位更新日期（不包含时分秒） 这个函数会返回一个date对象
def get_job_update_date(tree):
    date_text = tree.xpath('//span[@class="summary-plane__time"]/text()')[0]
    # print(f"{date_text=}")
    # 运行后会发现，有些岗位的更新时间会显示为今天，有些是几月几日，并且没有时分秒
    #接下来需要考虑：怎么对提取出的日期文本进行解析呢
    #而且如果跨年的时候，解析逻辑可能会报错，所以要用try exception捕捉
    #我们的目标是：把日期字符串解析成日期对象，比如datetime.date
    #日期对象就是为处理日期而设计的数据结构，也方便在需要的时候进行比较和计算
    try:
        #先调用date.today，拿到今天的日期
        today = date.today()
        if '今天' in date_text:
            update_date = today
        elif '月' in date_text and '日' in date_text:
            #用replace把字符串里的“更新于”替换为空字符串
            date_text = date_text.replace('更新于', '')
            year = today.year
            #先用正则获取到月份数字，再判断是否需要把年份减1，最后把中文日期拼接成YYYY年MM月DD日的完整字符串
            #最后用datetime.strptime转成date对象
            match = re.search(r"(\d+)月",date_text)
            update_date_month = int(match.group(1))
            if update_date_month > today.month:
                year = today.year-1
            date_text = f"{year}年{date_text}"
            dt = datetime.strptime(date_text, "%Y年%m月%d日")#y一定要大写，如果是小写，就是两位的年份，会导致解析失败或被错误解析
            #然后我们调用解析出的时间对象的date方法，取出不带时分秒的date对象
            update_date = dt.date()
        else:
            #如果date_text既不是今天，又不含月和日，说明不是我们认识的格式，直接抛出异常，交给外层统一处理
            raise Exception

        #最后如果没有异常出现的话，我们打印一下结果,并返回解析出的日期对象
        # print(f"{update_date=}")
        return update_date
    except Exception as e:
        # raise Exception(f"解析岗位更新时间失败，date_text：{date_text},e:{e}")
        print(f"解析岗位更新时间失败，date_text：{date_text},e:{e}")


#解析详情页
def parse_detail_page(page_url,job_region_dict):#第一个是网页url，第二个是字典，是从列表页抓取到的城市、区、街道
    #之所以把地点字典一并传入，是因为前面已经明确这一项是以列表页为准，但其余字段都会从详情页获取
    try:
        response = requests.get(page_url, headers=headers)
        response.raise_for_status()
        tree = etree.HTML(response.text)

        #岗位更新时间
        job_update_date = get_job_update_date(tree)

        #岗位名称
        job_name = get_job_name(tree)

        #薪酬范围
        job_salary_dict = get_job_salary(tree)

        #要求的工作经验、要求的学历、雇佣方式和招聘人数
        job_aummary_info_dict = get_job_summary_info(tree)

        #岗位技能标签
        job_skills = get_job_skills(tree)

        #岗位描述
        job_desc = get_job_desc(tree)

    except Exception as e:
        #异常处理这块不做“吞掉异常并打印”的处理，而是把异常重新抛出
        #具体做法就是在except里面raise一个新的Exception,并把原始异常对象e加进报错信息
        #这样做的目的是把异常给回到调用的函数
        #因为详情页解析失败意味着这条数据无法保证完整性，如果只是打印一下错误然后让parse_search_page继续运行，很可能会把一部分正确，一部分缺失的
        #数据写入到数据库里，后面清洗会更麻烦
        #现在把异常抛出，外层的parse_search_page函数就会知道异常的存在，不会继续进行数据入库，而是执行他的异常处理逻辑，也就是打印出解析失败的信息
        
        raise Exception(f'解析详情页异常：{e}')


#提取岗位所在地
def get_job_region(job_item):
    #因为xpath的返回值是一个文本列表，所以还要用[0]取出里面第一个元素
    region_text = job_item.xpath(".//div[@class = 'jobinfo__other-info-item'][1]/span[1]/text()")[0]
    # print(f'region_text = {region_text}')
    #所在地三个部分是用一个特殊的符号点隔开的，所以可以用python的split方法
    region_split_list = region_text.split("·")
    #接下来要把列表里的内容一一对应到三个变量：city、district、street
    #但是这里有个细节需要注意，不同岗位的地区信息可能不一样，有些岗位只有城市和区，没有写街道
    #所以更稳妥的方法是，先把这三个变量给一个默认值为空字符串
    city,district,street = '','',''
    #然后用len获取分割结果的长度，根据长度来判断能不能安全取值
    len_region_split_list= len(region_split_list)
    if(len_region_split_list >= 1):
        city = region_split_list[0]
    if (len_region_split_list >= 2):
        district = region_split_list[1]
    if (len_region_split_list >= 3):
        street = region_split_list[2]
    #最后把这三个变量打包到一个字典里,然后返回
    region_dict = {
        "city": city,
        "district": district,
        "street": street,
    }
    #这样调用数据后就能得到结构化的数据，而不是一整段不规则字符串了
    # print(f'{region_dict=}')
    return region_dict


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
        # 3。提取岗位所在地
        for job_item in job_item_list:
            job_region_dict = get_job_region(job_item)
            #可以看到岗位所在地是一整段字符串，如果想要在数据库里做更灵活的筛选，需要进一步把它拆分成三个部分

            #4。提取详情页URL
            #不能直接用class等于jobinfo__name来匹配，因为这样就无法匹配到class里包含其他值的岗位，所以要用contain函数模糊匹配
            job_detail_url = job_item.xpath(".//a[contains(@class,'jobinfo__name')]/@href")[0]
            #因为每个岗位只对应一个详情页，所以直接取返回列表里的第一个元素
            # print(f'{job_detail_url=}')
            #5。解析详情页
            parse_detail_page(job_detail_url,job_region_dict)
                #接下来把’请求并解析详情页'的动作独立成一个函数
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