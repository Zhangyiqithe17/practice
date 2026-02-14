import requests
#用来发起HTTP请求
import json
#用来把接口返回的JSON文本解析成python数据结构
import re
#在处理JSONP响应，用正则把外层的回调函数壳子去掉
import datetime
#对时间戳进行转换
import time
#备用，后面做分页请求或限速时，可以适当sleep
import traceback
#用来打印完整堆栈，定位问题非常直观

