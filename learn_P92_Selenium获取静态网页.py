#先在代码里完成：浏览器驱动配置、浏览器窗口最大化、访问豆瓣电影榜单这些操作
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
service = Service('D:/SeleniumDriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("http://movie.douban.com/top250")
time.sleep(2)
#目标是把网页内容上的电影的排名、中文和外文标题、评分、评价人数提取出来，用selenium应该怎么做
#首先，所有电影信息都在class值为“grid_view”的有序列表，即ol标签下面，被li标签包围
#要定位html元素，可以用WebDriver对象的find_element方法或find_elements方法，它们都能从打开的网页里查找元素
    #find_element用来查找单个元素，只返回第一个找到的元素，找不到会抛出异常
    # find_elements用来批量查找元素，找不到会返回空列表

#可以先调用find_element，把class值为“grid_view”的ol元素找出来
#要定位HTML元素，还需要从Selenium的webdriver.common.by模块导入by，它可以给元素定位策略提供预定义好的标识常量
    #比如By.ID说明定位依据是HTML元素的id属性
    #By.CLASS_NAME说明定位依据是HTML元素的class属性
    #By.TAG_NAME说明定位依据是HTML标签名
ol_grid_view = driver.find_element(By.CLASS_NAME,"grid_view")
print(ol_grid_view)#打印出来可看到是一个WebElement的实例，代表网页中的一个元素，可用于进一步操作或提取数据
#要提取出有序列表下面的列表项，进一步调用WebElement对象的find_elements方法，表示从这个元素下面继续查找元素
li_list = ol_grid_view.find_elements(By.TAG_NAME,"li")#找出它下面所有li标签
print(len(li_list))#25

#接下来进一步提取出列表里所有li元素的文本，包括排名、标题、评分信息
#通过for循环迭代列表里各个元素
for li in li_list:
    try:
        rank = li.find_element(By.TAG_NAME,"em").text
    except Exception as e:
        rank = None
        print(f"出现异常：{e}")
        # 需要注意的是，因为find_element找不到标签会报错，所以要捕获一下异常
        #标题都在class值为“title”的span元素里，分为简体中文名和原始语言名，但是对于原名就是简体中文的那样来说，可能只会包含一个class值为title的span元素
            #所以我们可以先通过find_elements方法结合By.CLASS_NAME，批量找出这些元素
            #如果查找出来列表长度大于1，即至少包含一个元素，那么把里面第一个WebElement提取出来，并且通过text获取元素的文本，它就对应了简体中文标题
    title_element_list = li.find_elements(By.CLASS_NAME,"title")
    title_zh = title_element_list[0].text if len(title_element_list) >= 1 else None
            #原始语言标题也是类似做法
        # title_original = title_element_list[1].text if len(title_element_list) >= 2 else None
            #但需要注意的是，外文标题还需要做额外处理：因为文本还包含了开头的“/”，所以要把“/”替换成空字符串
    title_original = title_element_list[1].text.replace(" / ","") if len(title_element_list) >= 2 else None

    try:
        score = li.find_element(By.CLASS_NAME, "rating_num").text
    except Exception as e:
        score = None
        print(f"出现异常：{e}")

    # print(f"排名：{rank}，简中标题：{title_zh}，原始标题：{title_original}，评分：{score}")
    # print(f"排名：{rank}，评分：{score}")

#需要注意一点：WebElement的text属性不止包含本元素里所有文本，还会包含不论层级的所有子元素的文本
    #比如可以试一下打印出列表里各个li元素的text属性
    # print(li.text)
#当我们成功提取到元素后，不仅可以提取出元素文本，还可以提取出指定属性的属性值
    #比如这个class值为“rating_num”的元素，如果我们想要提取出property属性的值，可以调用webElement对象的get_attribute,参数传入属性名(包括class也可以这样操作)
score_element = li_list[1].find_element(By.CLASS_NAME,"rating_num")
score_property = score_element.get_attribute("property")
print(score_property)#从打印结果来看，获取到property属性值复合我们预期
#webElement对象的get_attribute方法，不止可以用来获取元素对象的属性，还可以获取元素的HTML
    #只需要把传入的属性名换成传入字符串“outerHTML”或“innerHTML”
        #outerHTML表示获取元素完整的HTML，包括自身标签、子元素、文本、注释等等
        #innerHTML表示获取元素内部的HTML，包括子元素、文本、注释等，但不包括自身标签
#比如，先查找到class值为“hd”的元素，然后分别打印出这个元素的outerHTML和innerHTML
# hd_element = li_list[1].find_element(By.CLASS_NAME,"hd")
# print(f"hd_element的innerHTML：{hd_element.get_attribute('innerHTML')}")
# print(f"hd_element的outerHTML：{hd_element.get_attribute('outerHTML')}")

#查找属于多个类的元素
#在HTML代码里，我们经常能看到class值里包含空格的标签，这种情况说明这个元素同时属于多个类，，每个由空格分隔的都是一个独立的类名
    #比如有一个class="grid-16-8 clearfix",这里grid-16-8和clearfix是两个不同的类，这种元素是否能借助By.CLASS_NAME查找到呢？

# div_grid = driver.find_element(By.CLASS_NAME,"grid-16-8 clearfix")
# print(div_grid.get_attribute("class"))
#运行后直接报错了，报错说明程序没有找到class值为“grid-16-8 clearfix”的元素，所以By.CLASS_NAME不支持同时用多个类名来查找元素

#这种情况下，可以用By.CSS_SELECTOR，以及对应传入一个组合类选择器，，格式为“.类名1.类名2"，表示同时匹配有类名1、类名2这些类的元素
# div_grid = driver.find_element(By.CSS_SELECTOR,".grid-16-8.clearfix")
# print(div_grid.get_attribute("class"))

#前面都是在通过By这个类里面的标识常量来查找元素，比如By.TAG_NAME、By.CLASS_NAME、By.CSS_SELECTOR
# 但是对于没有特定属性值且嵌套比较深的元素来说，可能要不断通过外层的父元素来提取内层的子元素
#前面我们是用Xpath来解决这个问题的，selenium也支持Xpath表达式，所以前面学的这里也能用到
    #具体来说，我们可以给find_element或find_elements的第一个参数传入By.XPATH,然后第二个参数传入XPath表达式
for li in li_list:
    try:
        rating_count = li.find_element(By.XPATH,".//div[@class = 'bd']/div[1]/span[4]").text
    except Exception as e:
        rating_count = None
        print(f"出现异常：{e}")
    print(f"共有{rating_count}")

#有时候我们要批量获取的元素包含不同的属性值，比如豆瓣电影榜单里表示星数的span元素，calss值可能是rating5-t、rating45-t，也有可能是其他
    #这种就无法通过固定的值精准查找了，这种情况我们仍然可以通过元素所在位置写出对应XPath表达式来查找
    #但是根据位置定位元素也容易受到布局调整的影响，特别有些网页可能频繁变化前端页面
    #另一种方法是利用By.CSS_SELECTOR的模糊匹配能力进行模糊查找，定位出那些属性值不完全确定的元素
        #具体方式是：我们给find_element或find_elements的第一个参数传入By.CSS_SELECTOR，然后第二个参数传入一个模糊选择器
        #模糊选择器的语法是这样的：
        #如果要找出任何位置包含了某个子字符串的属性值，用“[属性名*='属性值']”
            #比如要找出class里包含“btn-”的元素，对应的选择器是[class*='btn-']
        #如果要找出以某个子字符串开头的属性值，用"[属性名^='属性值']"
            #比如要找出使用HTTPS协议的链接，对应的选择是"[href^='https://']"
        #如果要找出以某个子字符串结尾的属性值，用"[属性名$='属性值']"
            #比如要找出使用HTTPS协议的链接，对应的选择是"[href$='.pdf']"

    #所以要找出这些表示评分星数的span元素
    #但是表示星数的标签下面，还有个class值是“rating_num”的标签，也是以“rating”开头，那么我们可以组合两个选择器
    start_element_list = li.find_elements(By.CSS_SELECTOR,"[class*='rating'][class$='-t']")
    for start_element in start_element_list:#因为是find_elements，所以要用for循环把列表里的元素遍历出来
        print(start_element.get_attribute("outerHTML"))#把查找出的元素的html打印出来



