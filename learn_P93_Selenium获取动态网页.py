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
import time
#虽然隐式等待非常适合处理元素加载时间不确定的情况，但是它会影响WebDriver生命周期内所有的查找，所以在复杂场景里最好优先用显式等待
#显式等待指的是程序在执行某个操作前，先等待某个特定条件满足后再继续执行，比如等待元素加载完成、等待元素可见、等待元素可点击、等待元素包含特定文本
    #它是针对特定元素或条件设置
#要用显式等待，需要导入WebDriverWait类和expected_conditions模块
from selenium.webdriver.support.ui import WebDriverWait
#它是显式等待的核心，可以让程序在执行下一步操作前等待特定条件的发生
from selenium.webdriver.support import expected_conditions as EC
#这个模块包含了很多用于显式等待的条件类，因为模块名很长，所以打击会设置别名EC

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
# driver.implicitly_wait(10)
#比如这里调用了implicitly_wait方法，传入10作为参数值，那么我们下面调用find_elements的时候会触发等待机制
    # 如果目标元素出现了就继续执行后续代码，如果没有出现就继续等待
    # 如果已经超出了指定的最长等待时间10秒后，元素仍查找不到，find_elements就会返回一个空列表

#要实现显式等待，我们需要先初始化一个WebDriverWait对象，第一个参数传入WebDriver实例对象，然后用timeout参数设置最大等待时间，单位也是秒
    #以及用poll_frequency设置检测条件的间隔时间
wait = WebDriverWait(driver,timeout=10,poll_frequency=0.2)
#接下来进一步调用WebDriverWait对象的until方法,里面要传入一个expected_conditions模块下的条件
#比较常见的条件有以下这些：
    #presence_of_element_located:元素存在于DOM中，换句话说就是该元素的HTML标签已经被解析并插入到了DOM中，DOM是浏览器内存中表示页面结构的树状数据结构（元素不一定可见）
    #visibility_of_element_located:表示元素存在且可见，换句话说就是元素不仅存在于DOM中，而且它当前是用户可见的，拥有正的宽度和高度且没有隐藏样式
    #所以如果我们只需要获取数据，而不需要关心显示状态的话，用presence_of_element_located作为等待条件就ok
    # 但是如果要模拟用户的点击或输入，就需要等待元素可见了，那么可以用visibility_of_element_located作为等待条件
    #element_to_be_clickable：表示元素是可点击的
    #title_contains:表示页面的标题包含了指定的文本
    #url_changes：表示当前URL发生了变化
    #text_to_be_present_in_element:表示元素包含了指定文本
#再接下来，条件接收的参数是一个元组，元组里面分别包含元素的定位方式，比如By.CLASS_NAME,以及定位值，也就是前面定位方式对应的值，比如“username”这个类名
    #如果找到了符合条件的元素，until会返回单个WebElement对象，而如果没有符合条件的元素，会抛出异常
#而presence_of_element_located与visibility_of_element_located还有对应的找出多个元素的条件
    #分别是presence_of_all_elements_located与visibility_of_all_elements_located
    #它们之前的区别是：前者等待一个匹配的元素达到条件，后者等待所有匹配的元素达到条件，因此返回的数据类型是WebElement对象组成的列表
# job_element_list = driver.find_elements(By.CSS_SELECTOR,".jname.text-cut")
job_element_list = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.jname.text-cut'))
)
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


