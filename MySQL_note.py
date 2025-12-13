from urllib.parse import uses_params

#sys是系统Schema，新手不要动
##还有另外两个自动创建的Schema，分别是sakila和world
#点击上方第四个图标可以创建数据库Schema
#Schema的命名风格推荐用全小写加下划线
#Charset是设置储存内容的字符编码格式，如果选错可能出现乱码，我们可选择utf8mb4格式(最底下那个）
    #它是真正完整的utf8，会用1~4个字节来表示一个字符
#后面的一个下拉列表是文字的排序规则，保持default默认就行
#然后点击apply按钮创建Schema，然后会弹出一个窗口，点击apply、finish继续

#然后左侧就会显示新创建的Schema，点击箭头可以折叠和展开Schema内容
#Tables里是Schema下面的表，在Table上点击鼠标右键弹出菜单，然后点击Create Table可以创建表结构
#在弹出的这个表结构页面中，我们可以填入表名，字符集还是选择utf8mb4,Engine(引擎)选InnoDB
#还可以在下方的comment中注释一下表格的用途

#接下来设置表的字段
#也就是表中会包含那些列，比如电影数据中标题就是一个字段
#前面学到，表里面需要有一个或多个特殊的列作为主键，主键的作用是唯一标识表中的每一行
#那么我们可以设置一个叫id的字段作为这张表的主键，因为它不能重复，常规做法是把id这一列设置成数据类型为int整型的自增长的字段
#PK是primary key，表示主键
#勾选PK时，NN会自动勾选上，它是Not Null，表示字段内容不能为空
#UQ是Unique ，表示字段内容被不能重复，如果一个字段已经被勾选上主键了，我们可以不勾选UQ，因为主键约束自动包含唯一约束
#B是BINARY，是一种表示固定长度二进制字符串的数据类型，用于储存原始字节数据，比如图片哈希值（新手不用管，一般用不到）
#UN是unsigned，表示无符号数字，也就是只能是0或者正数
#ZF是ZERO FILL，0填充，也就是当字段类型为整数时，会在显示时用0填充至指定长度，比如98 0填充到5位显示00098
#AI是Auto Incremental 即自增，插入记录时这个字段值会自动递增
#G是Generated Column，表示自动生成列，如果给字段勾选了这一项，就表示这个字段的内容不是手动插入的
    #而是由其他字段组合运算得到的，比如如果价格和数量都会被手动插入的话，可以给总价字段勾选上G
    #然后在后面的Expression中填入运算表达式价格*数量，那么在写入一条记录时就会根据这个表达式自动计算出
    #总价的值并写入
#后面的Default/Expression用来设置字段的默认值或表达式
#下面的comment是注释，可以填入来标注字段的作用
#点击字段下的空白处，就可以增加新的字段

#Datatype
#Varchar，即可变长度的字符串，小括号里的数值表示最长长度的字节数，具体能储存多少汉字就和设置的字符集编码有关了
    #utf8mb4一般占3~4个字节，可以按4个字节计算，45字节能储存11个汉字
#DECIMAL，是储存精确浮点数的最佳选择，小括号里填入的内容要用逗号分割，比如DECIMAL(2,1)
    #逗号前的数字表示所占的总位数，会包括整数部分和小数部分，逗号后的数字表示小数部分保留的位数
    #所以DECIMAL(2,1)表示数字最多只能有两位数，并且小数点后可以保留一位

#一般像一部电影对应多个导演，这种非一对一关系的类型，包括了一对一或多对多，我们可以创建多张表来储存信息，然后在需要的时候做链接查询
    #也就是基于关系组合来自两个或多个表的信息
    #所以我们还要新创建一个表来储存导演数据，让两张表形成对应的关系
    #先把目前的表点击apply按钮创建表，在弹出的SQL语句窗口中直接点击apply、finish按钮执行SQL，把表创建出来
    #然后在左侧Tables中可找到新创建的表，也可看到表里面的字段列表

#接下来创建储存导演数据的表，依然是点击Create Table
#信息设置完开始设置字段，主键是必不可少的，所以还是先填入一个自增长的id字段,勾选PK、NN、AI
#接下来还要两个新增的字段，分别要对应电影id和导演名，这样就能把电影和指导的导演关联起来，也能通过导演查询出指导过的电影
#新增字段movie_id，这个字段储存的对应top250_douban这张主表里面的id字段，要勾选NN，让这个字段的内容不能为空
#新增字段director，勾选NN
#这里并没有给movie_id和director勾选UQ，表示不能重复，因为一部电影可以对应多个导演，一个导演也可以指导多部电影
    #但是我们并不希望同一部电影的同一位导演在这里重复，所以可以加一个联合索引，把这个联合索引设置为UQ
    #让这两个字段组合在一起不能重复
    #具体的做法是：点击编辑表格窗口下的Indexs，也就是索引选项卡
    #在切换后的窗口中可以看到已经存在一个名为Primary的索引，这个是创建主键字段时自动创建的主键索引
    #我们在主键索引下输入新索引名，比如unique_movied_director,Type选择UNIQUE
    #Index Colums中选择字段，把movie_id和director都勾选上
    #在Index comment框里还可以填写一下注释，比如限制同一个电影下的导演不能重复
    #然后点击apply按钮创建表

#如何通过Python代码来连接数据库，以及写入和读取表里面的数据
#不需要更换编程语言或工具，就可以把数据储存逻辑无缝集成到现有的python工作流里
#要高效地操作关系型数据库，需要我们掌握一个ORM（Object Relational Mapping 对象关系映射）框架
#ORM时一种编程技术，用于把面向对象的代码和关系型数据库的数据，进行自动的转换和映射
#简单来说，就是一张表可以映射成一个python类，每一行可以映射成实例化的类对象，每一列可以映射成类的属性
#ORM框架通过抽象掉大部分底层SQL操作，让我们可以使用面向对象的方式操作数据库，而不用直接编写SQL语句
#这样做的好处时，减少我们要记忆的SQL语法，并且可以避免在Python里手动拼接SQL而导致错误，提高安全性和可维护性
#这里要学习的ORM时第三方库Peewee，它以轻量、简洁、高效为核心，适配MySQL、PostgreSQL、SQLite等主流数据库
#在使用Peewee前，我们要安装一个MySQL数据库的链接驱动，比如mysqlclient
#因为Peewee连接MySQL时需要依赖这些驱动
#所以在终端输入pip install mysqlclient 如果安装失败可以安装pymysql
#接着安装peewee pip install peewee

#接下来进入到python代码的编写了
#首先创建一个数据库连接
#前面在用MySQL Workbench 创建Schema和表之前，我们先对MySQL数据库实例进行了连接，那么用peewee也是一样
#连接MySQL数据库需要导入peewee的MySQLDatabase类
from peewee import MySQLDatabase
#实例化MySQLDatabase时，我们需要传递这几个参数
#database：表示要连接的数据库名称
#在MySQL中，database也等同于Schema，但是Database会更多用来描述物理储存的层面，而Schema会更多用来描述逻辑结构，比如表的关系等
#host表示数据库服务器的IP地址，参数里的localhost表示本机
#port表示MySQL的端口号
#user表示连接数据库使用的账号，可以是前面创建的admin或root
#password表示连接数据库使用的密码，注意要设定为对应账号的密码
db = MySQLDatabase(
    database='spider_db',
    host='localhost',
    port=3306,
    user='root',
    password = '17170709',
)
#但是实例化MySQLDatabase时没有执行连接数据库的实际操作，所以我们还要调用connect方法进行连接
#如果连接成功，connect方法不会返回任何值，但是失败的话会抛出异常
#所以我们可以用try except捕获并打印异常信息
try:
    db.connect()
except Exception as e:
    print(f'连接数据库失败:{e}')
#但是我们需要了解的是，MySQL服务器实例的连接数是有数量限制的，由MySQL配置中的max_connections参数控制
#默认的最大连接数是151，我们每次调用connect方法成功连接后，就会占用一个连接数，而且哪怕程序执行完成了
#和MySQL的连接也不会立刻断开，而是会保持到超时才断开，默认是8小时
#那么一旦连接数达到了上限，再使用connect方法连接时就会抛出异常，提示由于‘Too many connections’而无法连接
#所以我们要养成一个好习惯是：打开的连接在使用完成后，及时调用close方法关闭掉

db.close()
#后续所有对数据库的操作，我们都会写在connect和close的调用之间
print(f"是否已关闭连接:{db.is_closed()}")





