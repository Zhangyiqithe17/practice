from openpyxl import Workbook#不需要设置样式，只需要导入这个类
#from openpyxl.style import Font,PatternFill#如果需要设置字体、背景颜色之类需要导入这些类
#一个工作簿（Workbook）可以有多张工作表（Worksheet）

#先实例化一个对象
wb = Workbook()#Workbook对象代表工作簿 新创建的工作簿默认会包含一个工作表
ws = wb.active#这个属性，得到工作簿当前活动的工作表，即用户打开Excel时默认选中的工作表
#因为active属性返回的数据类型是Worksheet对象，可以赋值给一个ws变量,之后就可以通过这个对象向对应的工作表中读写数据了
#比如可对ws的title属性赋值，来修改工作表的标签名称
ws.title = '豆瓣电影top250'
#接下来可以在工作表的表头，即第一行写入数据
headers = ['排名','电影名称','评分','年份']
#先创建一个储存表头的列表headers，然后通过for循环来依次写入每个列名
for i in range(len(headers)):
    header = headers[i]
    #要写入数据，我们需要能表示写入位置，即第几行第几列，但excel的行号和列号是从1开始的，这个和python里索引从0开始有区别
    col_num = i + 1
    #所以让表示列数的col_num变量在i的基础上加1
    cell = ws.cell(row=1, column=col_num)
    #然后调用ws的cell方法，通过指定行号row和列号column，得到对应位置的Cell对象，也就是表示单元格的对象
    cell.value = header
    #然后通过设置cell对象的value属性，给单元格写入数据值,也就是列名
wb.save('豆瓣电影Top250.xlsx')
#数据写好后就可以用工作簿对象wb的save方法来保存excel文件了



