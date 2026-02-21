#先在代码里完成：浏览器驱动配置、浏览器窗口最大化、访问豆瓣电影榜单这些操作
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

service = Service('D:/SeleniumDriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("http://movie.douban.com/top250")
time.sleep(2)