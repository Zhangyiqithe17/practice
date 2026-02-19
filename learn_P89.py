#用多线程并发请求所有网页并解析
#先创建豆瓣爬虫代码副本
import csv
from enum import Enum
import json
import re
import requests

from lxml import etree
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side

#先导入需要用到的类
from peewee import MySQLDatabase, Model
from peewee import AutoField,CharField,IntegerField,DecimalField

#导入线程管理要用到的类
from concurrent.futures import ThreadPoolExecutor


# 表示写入文件的类型的枚举类
#因为MySQL是一种新的储存类型，所以在枚举类型中增加新的类型
class WriteToType(Enum):
    CSV = 1
    JSON = 2
    EXCEL = 3
    MYSQL = 4

#创建一个全局变量db，用来表示数据库连接对象，然后实例化一个MySQLDatabase对象，赋值给变量db
db = MySQLDatabase(
    database='spider_db',
    host='localhost',
    port=3306,
    user='root',
    password = '17170709',
)
#接下来创建两张电影表对应的模型类
class Movie(Model):
    id = AutoField()
    rank = IntegerField(unique=True)
    title = CharField(max_length=100,
                      unique=True)
    score = DecimalField(decimal_places=1,
                         max_digits=2)
    year = IntegerField()
    rating_count = IntegerField()

    class Meta:
        database = db
        db_table = 'top250_douban_MYSQL'

class MovieDirectors(Model):
    id = AutoField()
    movie_id = IntegerField()
    director = CharField(max_length=100)
    class Meta:
        database = db
        db_table = 'top250_douban_directors_MYSQL'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
url = "https://movie.douban.com/top250"

#接下来创建一个可以把电影数据写入到MySQL数据库的函数,只接受movies列表作为参数
def write_movies_to_mysql(movies):
    try:
        db.connect()
        try:
            Movie.create_table(safe=True)
        except Exception as e:
            print(f"创建表发生异常:{e}")

        try:
            MovieDirectors.create_table(safe=True)
        except Exception as e:
            print(f"创建表发生异常:{e}")

    except Exception as e:
        print(f'数据库连接失败：{e}')
        return

    #事务处理
    with db.atomic():
        for movie_dic in movies:
            movie = Movie.create(rank = movie_dic['排名'],
                                 title = movie_dic['标题'],
                                 score = movie_dic['评分'],
                                 year = movie_dic['年份'],
                                 rating_count = movie_dic['评价人数'])
            #如果create没有抛出任何异常，说明数据写入成功了，我们把写入电影的标题和记录的id1打印出来
            print(f'电影：{movie.title} id：{movie.id}')
            #注意这里我们没有人为捕获create方法抛出来的异常，因为这样的话db.automic才会在异常出现后自动回滚整个事务

            #接下来导演记录的写入也是一样的逻辑
            #我们从movie_dic中获取导演列表，然后依次迭代列表里面各个导演名
            director_list = movie_dic['导演']
            for director_name in director_list:
                director_obj = MovieDirectors.create(director = director_name,movie_id = movie.id)
                print(f'电影：{director_obj.movie_id} id：{director_obj.director}')




# 储存所有电影信息到CSV文件
def write_movies_to_csv(movies):
    with open('douban_top250_movies.csv', 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ["排名", "标题", "评分", "年份", "评价人数", "导演"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(movies)
    print("电影信息已写入 douban_top250_movies.csv")


# 储存所有电影信息到JSON文件
def write_movies_to_json(movies):
    with open('douban_top250_movies.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    print("电影信息已写入 douban_top250_movies.json")

# 储存所有电影信息到Excel文件
def write_movies_to_excel(movies):
    wb = Workbook()
    ws = wb.active
    ws.title = "豆瓣电影Top250"
    excel_headers = ["排名", "标题", "评分", "年份", "评价人数", "导演"]
    thin_side = Side(style='thin')
    for col_num, header in enumerate(excel_headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True)
        cell.border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    for movie in movies:
        ws.append(list(movie.values()))

    wb.save('douban_top250_movies.xlsx')
    print("电影信息已写入 douban_top250_movies.xlsx")



# 获取电影标题
def get_title(item):
    title_elements = item.xpath('.//div[@class="hd"]/a/span[1]/text()')
    title = title_elements[0] if title_elements else None
    return title


# 获取电影评分
def get_score(item):
    score_elements = item.xpath('.//span[@class="rating_num"]/text()')
    score = score_elements[0] if score_elements else None
    return score


# 获取电影排名
def get_rank(item):
    rank_elements = item.xpath('.//div[@class="pic"]/em')
    rank_html = etree.tostring(rank_elements[0], encoding="unicode").strip() if rank_elements else None
    rank_match = re.search(r'\d+', rank_html)
    rank = rank_match.group() if rank_match else None
    return rank


# 获取电影评价人数
def get_rating_count(item):
    rating_count_elements = item.xpath('.//div[@class="bd"]//span[4]/text()')
    rating_count_text = rating_count_elements[0] if rating_count_elements else None
    rating_count_match = re.search(r'\d+', rating_count_text)
    rating_count = rating_count_match.group() if rating_count_match else None
    return rating_count


# 获取包含电影导演和年份的文本
def get_director_and_year_group_text(item):
    director_elements = item.xpath('.//div[@class="bd"]/p[1]/text()')
    director_text = director_elements[0].strip() if director_elements else None
    year_text = director_elements[1].strip() if len(director_elements) == 2 else None
    return director_text, year_text


# 获取电影年份
def get_year(year_text):
    year_match = re.search(r'\d{4}', year_text)
    year = year_match.group() if year_match else "获取年份失败"
    return year


# 获取电影导演列表
def get_director_list(director_text):
    director_match = re.search(r'导演[：:]\s*(.*?)((\s{2,}主)|(\.{3}))', director_text)
    director_text = director_match.group(1).strip() if director_match else None
    director_list = director_text.split(" / ")
    # for director in director_list:
    #     print(f"导演: {director}")
    return director_list


# 遍历电影项列表并提取信息
def process_movie_items(movie_item_list, movies, write_to):
    for item in movie_item_list:
        # 获取标题
        title = get_title(item)
        # 获取评分
        score = get_score(item)
        # 获取排名
        rank = get_rank(item)
        # 获取评价人数
        rating_count = get_rating_count(item)
        # print(f"排名={rank}, 标题={title}, 评分={score}, 评价人数={rating_count}")
        # 获取年份和导演列表
        director_and_year_group_text = get_director_and_year_group_text(item)
        year = get_year(director_and_year_group_text[1])
        director_list = get_director_list(director_and_year_group_text[0])
        # 创建电影信息字典
        movie_dict = create_movie_dict(rank, title, score, year, rating_count, director_list, write_to)
        movies.append(movie_dict)
        # print(f"{movie_dict=}")
    return movies


# 获取HTML内容
def get_html_content(url_, start_=0):
    page_url = f"{url_}?start={start_}"
    response = requests.get(page_url, headers=headers)
    response.raise_for_status()
    html_content = response.text
    return html_content


# 创建电影信息字典
#接着修改这个函数，增加对枚举类型的判断
def create_movie_dict(rank, title, score, year, rating_count, director_list, write_to):
    if write_to == WriteToType.JSON or WriteToType.MYSQL:
        director_value = director_list
    #在写入数据库的情况下，和写入json一样，我们需要导演值以列表而不是字符串的形式存在
    else:
        director_value = ",".join(director_list)
    movie_dict = {
        "排名": rank,
        "标题": title,
        "评分": score,
        "年份": year,
        "评价人数": rating_count,
        "导演": director_value,
    }
    return movie_dict

#接下来找到scrape_top250_movies这个函数，它是实际执行爬虫的主要函数
#思路是创建多条线程，然后让每个线程去负责一部分的网页爬取和解析，这样当某些线程在等待网络响应的时候，不会耽误另外一些线程获取HTML源代码
    #可以更高效获取多个页面的数据
    #可以把任务大致划分为获取网页HTML内容和解析网页内容
def scrape_top250_movies(write_to):
    movies = []
    #先来创建一个用来储存提交获取网页HTML任务后，所返回的Future对象的列表
    html_future_list = []
    try:
        #然后创建线程池
        #要注意线程数量太多可能导致网站压力，豆瓣是一个流量比较多的网站，但是并发过多可能触发一些网站的反爬虫机制，导致IP被封禁
        #而且如果我们爬取的数据量很大，并发还设置过高的话，可能造成某些中小型网站瘫痪或没法正常提供服务，万一网站运营方报j就不好
        #所以我们可以先把线程数上限先调成3看看效果
        #然后把原有的爬取各个页面HTML的for循环也放入到with块里
        with ThreadPoolExecutor(max_workers=3) as pool:
            for start in range(0, 250, 25):
                # html = get_html_content(url, start)
                #获取HTML内容主要是通过这个get_html_content函数实现的，所以要把这里的串行请求改为并行请求
                #调用线程池的submit方法，第一个参数传入get_html_content,作为线程要完成的任务
                # 然后get_html_content原本会接收的两个参数url和start，也按照顺序传入到submit方法里
                #submit方法会返回一个Future对象，我们添加到前面创建好的html_future_list里
                html_future = pool.submit(get_html_content, url, start)
                html_future_list.append(html_future)
                #接下来修改XPath解析电影数据这部分，创建列表变量movie_items_future_list,用于储存submit方法返回的Future对象
                #需要储存的原因是，get_html_content会返回发送请求后获取到的HTML内容,所以我们执行完之后要查看执行结果

                #那么我们用for循环来迭代html_future_list里的每一个Future对象，然后调用对象的result方法，获取到各个页面的html源码
                for html_future in html_future_list:
                    tree = etree.HTML(html_future.result())
                    # tree = etree.HTML(html)
                    item_list = tree.xpath('//div[@class="item"]')
                    movies = process_movie_items(item_list, movies, write_to)
                #到目前为止，获得网页html这个任务已经转换成多线程执行了

        if write_to == WriteToType.CSV:
            write_movies_to_csv(movies)
        elif write_to == WriteToType.JSON:
            write_movies_to_json(movies)
        elif write_to == WriteToType.EXCEL:
            write_movies_to_excel(movies)
        #然后在文件写入这里，增加一个对MySQL写入类型的判断，以及对应函数的调用
        elif write_to == WriteToType.MYSQL:
            write_movies_to_mysql(movies)
        else:
            print("未实现的写入文件类型：", write_to)
    except requests.RequestException as e:
        print(f"请求失败: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

#最后为了验证写入逻辑，把主程序入口里的写入类型也修改为MySQL
if __name__ == '__main__':
    scrape_top250_movies(WriteToType.MYSQL)

#在workbench窗口可以手动删除记录:
#点击要操作的某行记录，鼠标右键，点击Delete Row(s),然后点击Apply，在弹出的窗口中继续Apply、Finish