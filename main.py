import requests

if __name__ == '__main__':
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
        }
        url = 'https://www.zhaopin.com/sou/jl765/kwE8M8CQO/p1'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(response.text)
        #这就是网页服务器返回的HTML代码
    except Exception as e:
        print(e)

    #如果在运行结果里看到了完整的HTML，那么就可以进行下一步了
    #但是像现在这个代码的运行结果一样：响应的结果里只有一点点HTML，而且还可以看到像TCaptcha.js这样的关键词，就基本可以判断：
    #我们的情趣被网站的风控识别成了不可信，于是被重定向到了验证码页面
    #所以我们要把请求伪装得更像真是浏览器，看看能否绕过这类基础校验