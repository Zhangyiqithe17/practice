#接下来学会掌握用selenium控制键盘输入的进阶技能，让程序不仅能打开网页，还能像真人一样在网页上输入文字、按下回车键、甚至实现全选、删除、复制粘贴等快捷操作
#如果要给网页上的输入框输入文字，基本思路是：
    #先用find_element找到输入框对应的WebElement
    #然后调用元素的send_keys方法，把文字输入进去

#比如，在豆瓣首页的登录框里，可以看到手机号输入框对应的这个<input>标签，name属性是phone，以及验证码输入框对应这个<input>标签，id属性是code
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
service = Service('D:\SeleniumDriver\chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("http://www.douban.com/")