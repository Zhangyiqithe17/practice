#到目前为止，我们掌握了从网页上获取静态数据的技能，但是如果面对动态加载的数据，怎么处理呢?
#因为豆瓣电影top250是静态数据，所以调用WebDriver对象的get方法访问网页后，我们可以直接查找HTML元素
#但如果我们所需的数据是动态加载到网页上的，那么如果调用get方法后立刻查找元素，有可能是找不到结果的
    #因为时间差很短的情况下，动态加载数据可能还没来得及被加载到网页上
    #例如前程无忧这个网站的搜索界面，打开网页HTML源代码后，一个岗位相关名称都看不到，说明这就是一个动态网页
from openpyxl.utils.datetime import time_to_days
#经过分析可以发现，包含岗位名称的span元素，class属性的值都是“jname text-cut”
    #所以还是用WebDriver对象的get方法请求这个URL，然后进一步调用这个find_elements方法
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service('D:/SeleniumDriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get('https://we.51job.com/pc/search')
#对此最简单的方法是暂停运行，也就是在get方法执行完成后，让程序暂停n秒，这个n的值可以根据网速和页面加载速度来主观决定
    #但总之目标是让动态数据在程序暂停的时间里，能够加载到网页上
# time.sleep(5)
# #虽然能成功，但是这种方式并不是很稳健，因为非常容易受网络环境波动和加载数据大小的影响

#selenium的WebDriver对象有一个叫implicitly_wait的方法，它可以实现隐式等待
    #隐式等待是Selenium的一种全局等待策略，它会影响后续所有元素定位操作，包括find_element、find_elements
    #具体来说，当我们设置了隐式等待时间后，如果元素立即存在，driver会立即执行下一步操作，不会额外等待
    #而如果元素还不存在，driver就会在指定的时间内定时重复查找元素，直到元素出现了或超时了
start = time.time()
driver.implicitly_wait(10)
#比如这里调用了implicitly_wait方法，传入10作为参数值，那么我们下面调用find_elements的时候会触发等待机制
    # 如果目标元素出现了就继续执行后续代码，如果没有出现就继续等待
    # 如果已经超出了指定的最长等待时间10秒后，元素仍查找不到，find_elements就会返回一个空列表
job_element_list = driver.find_elements(By.CSS_SELECTOR,".jname.text-cut")
duration = time.time() - start
print(f"程序等待了{duration:.2f}秒")
#然后把查找出的span元素的数量和里面的文本内容打印出来
print(f"共找到{len(job_element_list)}个元素")
for job_element in job_element_list:
    print(job_element.text)
#从打印结果中可以看到，共查找到0个元素，说明执行find_elements方法时，岗位相关数据还没有加载到网页上

#从等待结果来看，隐式等待在等待时间合理的情况下，也帮我们成功获取到了页面上岗位的名称
    #如果想知道隐式等等具体的等待时长，也可以通过time模块的time函数，记录从等待开始到结束的时间差

#需要注意的是，当我们给WebDriver实例设置了隐式等待后，所有通过这个driver执行的find_element、find_elements,都会被自动注入相同的等待逻辑
    #不需要每次查找元素时都单独写等待代码了，相应的，如果元素不是立即出现，driver都会持续等待直到元素出现或超时


