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

    print(f"排名：{rank}，简中标题：{title_zh}，原始标题：{title_original}，评分：{score}")
    # print(f"排名：{rank}，评分：{score}")