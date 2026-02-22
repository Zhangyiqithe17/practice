#到目前为止，我们掌握了从网页上获取静态数据的技能，但是如果面对动态加载的数据，怎么处理呢?
#因为豆瓣电影top250是静态数据，所以调用WebDriver对象的get方法访问网页后，我们可以直接查找HTML元素
#但如果我们所需的数据是动态加载到网页上的，那么如果调用get方法后立刻查找元素，有可能是找不到结果的
    #因为时间差很短的情况下，动态加载数据可能还没来得及被加载到网页上
    #例如前程无忧这个网站的搜索界面，打开网页HTML源代码后，一个岗位相关名称都看不到，说明这就是一个动态网页

#经过分析可以发现，包含岗位名称的span元素，class属性的值都是“jname text-cut”
    #所以还是用WebDriver对象的get方法请求这个URL，然后进一步调用这个find_elements方法
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service('D:/SeleniumDriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get('https://www.51job.com/pc/search')

job_element_list = driver.find_elements(By.CSS_SELECTOR,".jname.text-cut")
#然后把查找出的span元素的数量和里面的文本内容打印出来
print(f"共找到{len(job_element_list)}个元素")
for job_element in job_element_list:
    print(job_element.text)
#从打印结果中可以看到，共查找到0个元素，说明执行find_elements方法时，岗位相关数据还没有加载到网页上

