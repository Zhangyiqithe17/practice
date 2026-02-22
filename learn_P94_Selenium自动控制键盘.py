#接下来学会掌握用selenium控制键盘输入的进阶技能，让程序不仅能打开网页，还能像真人一样在网页上输入文字、按下回车键、甚至实现全选、删除、复制粘贴等快捷操作
#如果要给网页上的输入框输入文字，基本思路是：
    #先用find_element找到输入框对应的WebElement
    #然后调用元素的send_keys方法，把文字输入进去

#比如，在豆瓣首页的登录框里，可以看到手机号输入框对应的这个<input>标签，name属性是phone，以及验证码输入框对应这个<input>标签，id属性是code
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service('D:\SeleniumDriver\chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("http://www.douban.com/")

# phone_element = driver.find_elements(By.NAME,"phone")#根据name的值找到手机号输入框
# phone_element.send_keys("123456")#调用元素的send_keys方法，参数传入要在输入框里输入的内容
#但是如果运行这段代码，会发现程序报错了，提示找不到元素
#这是因为手机号输入框被包裹在了iframe标签里，iframe就像是网页中的一个小网页
# 所以如果不先切换到这个iframe，selenium只会盯着主页面查找元素，于是就找不到iframe里的输入框

#所以我们需要先进行这个切换到iframe的操作，这里可以先用Xpath定位这个iframe元素
    #它是class值为“login”的div下的第一个iframe
iframe_element = driver.find_element(By.XPATH,"//div[@class = 'login']/iframe[1]")
#然后调用driver的switch_to.frame方法，切换到iframe
    #这里的switch_to.frame是Selenium提供的专门用来“切换上下文”的方法，可以理解为视角从“主页”这个大房子，转移到iframe这个小房间，只有进入其内部才能继续访问里面的元素
driver.switch_to.frame(iframe_element)
phone_element = driver.find_element(By.NAME,"phone")#根据name的值找到手机号输入框
code_element = driver.find_element(By.ID,"code")#验证码输入框
phone_element.send_keys("123456")#调用元素的send_keys方法，参数传入要在输入框里输入的内容
code_element.send_keys("123456")#调用元素的send_keys方法，参数传入要在输入框里输入的内容

time.sleep(3)