#接下来学会掌握用selenium控制键盘输入的进阶技能，让程序不仅能打开网页，还能像真人一样在网页上输入文字、按下回车键、甚至实现全选、删除、复制粘贴等快捷操作
#如果要给网页上的输入框输入文字，基本思路是：
    #先用find_element找到输入框对应的WebElement
    #然后调用元素的send_keys方法，把文字输入进去

#比如，在豆瓣首页的登录框里，可以看到手机号输入框对应的这个<input>标签，name属性是phone，以及验证码输入框对应这个<input>标签，id属性是code
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
#还有一些网页交互需要双击鼠标才能触发，比如在输入框里双击选中内容、在表格里双击进入编辑模式等
#selenium提供了一个专门用于处理复杂鼠标交互的类：ActionChains
    #它可以把一系列鼠标和键盘动作组合成一条动作链，比如在某个元素上按下鼠标不松开，然后移动鼠标拖拽该元素到指定位置，然后再松开鼠标，这三个动作就是一个动作链
    #虽然拖拽、悬停等涉及多个动作组合，但双击是最简单的一种，因为只包含一个动作
    #假如我们目标是在豆瓣密码登录模块上的手机号/邮箱输入框里，输入一些内容，然后通过双击操作选中文字，那么首先需要
        #从Selenium.webdriver.common.action_chains模块里，导入ActionChains
from selenium.webdriver.common.action_chains import ActionChains

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
# iframe_element = driver.find_element(By.XPATH,"//div[@class = 'login']/iframe[1]")
#然后调用driver的switch_to.frame方法，切换到iframe
    #这里的switch_to.frame是Selenium提供的专门用来“切换上下文”的方法，可以理解为视角从“主页”这个大房子，转移到iframe这个小房间，只有进入其内部才能继续访问里面的元素
# driver.switch_to.frame(iframe_element)
# phone_element = driver.find_element(By.NAME,"phone")#根据name的值找到手机号输入框
# code_element = driver.find_element(By.ID,"code")#验证码输入框
# phone_element.send_keys("123456")#调用元素的send_keys方法，参数传入要在输入框里输入的内容
# code_element.send_keys("123456")#调用元素的send_keys方法，参数传入要在输入框里输入的内容
#
# time.sleep(1)

#除了向输入框输入字符串，我们还可以模拟键盘上一些“功能键”，比如回车键、删除键、全选键之类的操作
#接下来可以模拟按下回车键，让程序自动提交表单
#这个操作很简单，我们只需要借助Keys类，它提供了很多常见按键的模拟方式，所以我们需要先对Keys类进行导入
#然后调用验证码输入框对象的send_keys方法，然后传入Keys.ENTER作为参数，这就相当于在验证码输入框里按下回车了
# code_element.send_keys(Keys.ENTER)
#除了回车键之外，Keys类还有很多按键
    #Keys.ENTER表示回车
    #Keys.BACKSPACE表示退格
    #Keys.CONTROL表示Ctrl等等

#还可以在输入框里用快捷键Ctrl+A实现全选操作
    #还是调用send_keys方法，参数传入Keys.CONTROL，表示control键，以及“+”号，后面跟上字符“a”，组合起来就等效于按下了Ctrl+A来全选内容
# code_element.send_keys(Keys.CONTROL+'a')
    #举一反三，参数传入Keys.CONTROL+'c'可以实现复制，参数传入Keys.CONTROL+'v'可以实现粘贴等
    #如果电脑是MacOS系统，需要把Keys.CONTROL替换成Keys.COMMAND

#运行程序后可以看到，验证码输入框里的内容被全选了

#如果想要往已经填写内容的输入框里，继续输入字符串，只需要再一次调用对象的send_keys方法，send_keys的默认行为是不清空原内容，而是在末尾追加
# phone_element.send_keys("789")

#如果想实现的是覆盖输入而不是追加输入的话，有多种方法可以实现
    #1、先用Ctrl+A全选输入框中的内容，然后按下删除键，对应Keys.BACKSPACE，最后向输入框中输入新的内容
# time.sleep(3)
# phone_element.send_keys(Keys.CONTROL+'a')
# phone_element.send_keys(Keys.BACKSPACE)#这一步也可以省略，因为全选后输入新的内容也会把之前输入的覆盖掉
# phone_element.send_keys("17176666")
            #但这个方法的缺点是：写代码时要额外考虑操作系统
    #2、所以更推荐的删除方法是调用元素的clear方法，这个方法可以直接清空输入框，不需要模拟键盘操作,也不需要考虑操作系统差异
# phone_element.clear()
# phone_element.send_keys("17176666")
# time.sleep(3)

#Selenium模拟鼠标操作
    #鼠标操作能帮我们完成网页上的点击、双击、右键、悬停、拖拽等动作，让程序像真人一样和网页进行更复杂的交互
        #比如点击登录按钮、拖动滑块验证码、拖拽文件到上传区域
    #在访问一些内容比较多的网页时，比如以瀑布流形式加载的页面，我们经常需要手动滚动页面，才能看到更多内容，selenium也可以实现滚动操作

#具体来说，我们可以通过driver的execute_script方法，执行一段JavaScript代码来控制页面滚动
    #最常用的控制滚动的JavaScript代码是window.scrollBy(x,y);(要注意结尾有一个分号)，其中x表示横向滚动的像素数，y表示纵向滚动的像素数
        #如果是正数，表示向右或者向下滚动，如果是负数，表示向左或者向上滚动

#假设已经实现了通过Selenium访问豆瓣首页，那么接下来的目标是让程序控制浏览器向下滚动300像素的话，代码可以这样写：
# driver.execute_script("window.scrollBy(0,300);")
# time.sleep(3)
#运行程序后就会看到页面自动向下滚动的效果了

#有时候我们不知道目标内容举例顶部有多远，这时候更推荐的方法是：让页面自动滚动到某个元素的位置，直到它出现在我们的可视区域中
    #具体做法仍然是：调用driver的execute_script方法，来执行这段JavaScript代码
    #这次要执行的代码："arguments[0].scrollIntoView();",其中arguments[0]表示传入的第一个参数
    # scrollIntoView()表示让传入的那个元素滚动到页面的可视区域中

#如果在豆瓣首页，想要把页面滚动到下方的读书板块，那这个区域对应的HTML元素的ID是anony-book，那么我们可以
    #先调用WebDriver对象的find_element方法找到那个元素
# anony_book_element = driver.find_element(By.ID,"anony-book")
    #然后调用execute_script方法，执行arguments[0].scrollIntoView()这句JavaScript代码，以及把这个元素也作为参数传进去
# driver.execute_script("arguments[0].scrollIntoView();",anony_book_element)
#那么程序运行后就可以看到，页面被自动滚动到了读书板块对用户可见的位置

# time.sleep(3)

#在鼠标操作中，最常见的是左键点击
    #以豆瓣首页的登录模块为例子，在默认状态下显示的是“扫码登录”，而如果我们想切换到“密码登录”，就需要点击上方的密码登录选项卡
    #这个选项卡对应的HTML元素是一个li标签，类名是"account-tab-account",那么我们可以这样实现点击操作
        #首先还是通过find_element找到这个元素
        #然后调用click方法，模拟鼠标左键点击（需要注意的是，因为这个登录模块在iframe里，所以不要忘了要先找到这个iframe,切换到iframe，
            # 然后再在里面执行查找元素的操作）
iframe_element = driver.find_element(By.XPATH,"//div[@class = 'login']/iframe[1]")
driver.switch_to.frame(iframe_element)
tab_account_element = driver.find_element(By.CLASS_NAME,"account-tab-account")
tab_account_element.click()
# time.sleep(3)
#运行后就可以看到，程序帮我们通过点击操作，自动切换到了密码登录的选项卡

#接下来还是要找到目标元素，我们可以看到手机号/邮箱输入框对应这个<input>标签，name属性的值是username
    #那么在切换到iframe，点击密码登录选项卡后，调用find_element找到这个输入框，以及调用send_keys方法，随便输入一些文字
username_element = driver.find_element(By.ID,"username")
# username_element.send_keys("用户名")

#接下来是动作链的关键：要先实例化一个ActionChains对象来构建动作链，参数传入driver，也就是用来控制浏览器的WebDriver实例
    #这样ActionChains才知道要在哪个浏览器里执行这些动作
# actions = ActionChains(driver)
#下一步是添加双击动作
    #调用ActionChains对象的double_click方法，把我们想要双击的元素传进去
    #但是double_click方法只是添加了动作，并没有执行
    #所以添加完所有需要执行的动作后，我们还需要继续调用perform方法来实际执行这些动作
# actions.double_click(username_element).perform()
#所以总结下来就是：我们需要创建动作链对象、给动作链添加操作，以及执行动作链
#运行后就可以看到程序在目标输入框里执行了双击操作，于是输入内容里最后一个字被自动选中了

#如果想要把输入的内容全部选中，要怎么操作?
    #鼠标连续三次快速点击，就可以让浏览器把整段文字全部选中，selenium同样可以模拟这样的行为，只需要在刚才的双击动作后，再加一个单击动作，就可以模拟三击效果
    #即，可以把一个.double_click(...)和一个.click(...)操作串联起来，构成一个连续动作链，最后统一用.perform()执行整个链条
# actions.double_click(username_element).click(username_element).perform()
#三击运行成功

#除了点击，还可以用selenium模拟拖拽动作
#ActionChains对象的drag_and_drop方法，可以模拟把一个元素拖拽到另一个元素上
#豆瓣首页，如果把“找回密码”拖拽到手机号/邮箱输入框里面，页面会把这个链接的地址自动填入到输入框，这个交互就可以用drag_and_drop实现
    #还是需要先找到对应的元素
link_fwd_element = driver.find_element(By.CLASS_NAME,"fwd-link")
    #接下来创建动作链对象
actions = ActionChains(driver)
    #然后调用动作链对象提供的drag_and_drop方法，把a元素作为拖动源，输入框作为拖动到的目标，最后通过perform方法把这条动作链实际执行出来
actions.drag_and_drop(link_fwd_element,username_element).perform()
time.sleep(3)