from symtable import Class
from urllib.parse import uses_params

from openpyxl.styles.builtins import title
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

from peewee import MySQLDatabase, Model, CharField, ForeignKeyField

#实例化MySQLDatabase时，我们需要传递这几个参数
#database：表示要连接的数据库名称
#在MySQL中，database也等同于Schema，但是Database会更多用来描述物理储存的层面，而Schema会更多用来描述逻辑结构，比如表的关系等
#host表示数据库服务器的IP地址，参数里的localhost表示本机
#port表示MySQL的端口号
#user表示连接数据库使用的账号，可以是前面创建的admin或root
#password表示连接数据库使用的密码，注意要设定为对应账号的密码

#先导入peewee的Model类，它表示一个可以映射到数据表的数据模型
#然后我们要创建出对应电影数据表的类Movie，这个Movie类必须要继承peewee的Model类，让ORM框架发挥作用
#接下来要定义类的属性，类的属性会映射到数据表的字段，并且默认会和同名的数据表字段直接对应，所以这里可直接和数据表一样的字段名
#id、rank、title、score、year、rating_count等
#需要注意的是，这些属性不会定义在__init__方法里，而是作为类属性，直接定义在class的下面
#定义在_init__方法里的是对象属性，每个实例的对象属性的值是独立的，而类属性被这个类的所有实例共享
#接下来每个属性需要被赋值为peewee的字段类的实例,所以我们需要导入这些类
from peewee import AutoField,IntegerField,CharField,DecimalField
#字段类包括了AutoField:自增整数主键字段
#IntegerField:整数字段
#CharField:字符串字段
#DecimalField:精确小数字段
#当然字段类型实际上还有很多，包括
#BooleanField:布尔值字段
#DataField:日期字段
#DateTimeField:时间字段
#我们可以对照数据表里的字段来添加类属性

#连接数据库
#定义模型类
#查询所有表
#创建指定表
#删除指定表

db = MySQLDatabase(
    database='spider_db',
    host='localhost',
    port=3306,
    user='root',
    password = '17170709',
)


class Movie(Model):
    id = AutoField()  # id就可以被赋值为AutoField，表示主键，并默认为就是自增、唯一、非空的
    rank = IntegerField(unique=True)  # 表示排名的rank因为是整数，所以被赋值为IntegerField，另外把参数unique设置为True,和数据表里这个字段的唯一约束对应
    title = CharField(max_length=100,
                      unique=True)  # 表示标题的title是字符串，所以被赋值为CharField对象，以及这里也要设置max_length来定义最大长度，以及设置参数unique=True声明唯一约束
    score = DecimalField(decimal_places=1,
                         max_digits=2)  # 表示评分的score是精准小数，所以被赋值为DecimalField对象，参数max_digits用于设置总位数，decimal_places用于设置小数点后的位数
    year = IntegerField()  # 表示年份的year是整数，IntegerField对象
    rating_count = IntegerField()  # 表示评分人数的rating_count是整数，IntegerField对象
    # 当前我们所有的类属性名和数据表里的字段名是一致的，但是如果不同的话，也可以在实例化字段对象时，通过db_column参数手动设置字段名
    # 比如 用的是rank_num代替rank
    # rank_num = IntegerField(unique=True,db_column = 'rank'),这样手动指定映射关系

    # 在模型类的字段定义完毕后，我们通常会添加一个叫Meta的内部类，进行数据库相关配置
    # 内部类就是在类里面定义的类
    # Meta类中需要包含database类型和db_table属性
    # database属性是必须要有的，要赋值为已经初始化的Database实例，比如前面创建的MySQLDatabase的实例对象db
    #这是模型操作数据库的前提条件
    #db_table是可选属性，用来指定要操作的表名，所以要赋值为电影表的表名top250_douban
    #如果不定义db_table，peewee会默认操作把Class名转换为小写名字的表
    class Meta:
        database = db
        db_table = 'top250_douban'

#还有个记录导演信息的表top250_douban_directors,所以这里也把对应的模型MovieDirectors创建出来
class MovieDirectors(Model):
    id = AutoField()
    movie = IntegerField()
    director = CharField(max_length=100)
    class Meta:
        database = db
        db_table = 'top250_douban_directors'

#在了解如何通过peewee读写数据库之前，我们先了解一下如何通过peewee在数据库中创建表
#我们前面在MySQL Workbench做的那些点击操作，都是可以用代码来代替的
#首先仍然是要定义一个模型类，比如叫MovieTest，用于测试创建表，它里面的属性我们也照搬Movie模型类
#只是Meta类里的db_table属性可以移除，peewee会把类名MovieTest转为表名movieTest
class MovieTest(Model):
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



#但是实例化MySQLDatabase时没有执行连接数据库的实际操作，所以我们还要调用connect方法进行连接
#如果连接成功，connect方法不会返回任何值，但是失败的话会抛出异常
#所以我们可以用try except捕获并打印异常信息
try:
    db.connect()
    # 接下来实际进行创建操作，模型类create_table方法可以用来创建表
    # 我们还可以设置safe参数为True来防止重复创建表，因为这样当表已经存在时，就不会执行创建操作了
    # 如果创建成功的话，create_table什么都不会返回，而如果创建失败，方法会抛出异常，所以可以用try except进行捕获,让异常出现的时候程序不会中止
    try:
        MovieTest.create_table(safe=True)
    except Exception as e:
        print(f"创建表发生异常:{e}")

    # 如果没有出现异常，我们打开Workbench连接MySQL，应该可以在Table列表中看到新创建出来的movietest表
    # 如果没看到，可以点击SCHEMAS右边的刷新图标，或者右键Tables，选怎Refresh All
    #可以看到，为什么所有字段的NN都被勾选上了呢？，这是因为字段类被实例化的时候，null参数默认为False
    # 所以除非我们手动设置参数null=True，否则字段都会受到NOT NULL约束

    #我们还可以用peewee查询出Schema中所有的表
    #具体方式是调用DataBase对象的get_tables()方法，这个方法会返回一个列表，每个元素都是一个表名的字符串
    table_list = db.get_tables()
    print(table_list)

    #接着是删除表，可以用drop_table
    try:
        MovieTest.drop_table(safe=True)
        print(db.get_tables())
    except Exception as e:
        print(f"删除表发生异常:{e}")
    #删除的时候仍然可以设置safe参数为True，避免由于表不存在而抛出异常
    #drop_table和create_table一样，如果删除成功的话什么都不会返回，而如果删除失败的话，方法会抛出异常，所有还是要捕获异常
    #以及为了更直观地了解表删除是否成功，我们可以在删除操作前后打印出get_tables的调用结果


    try:
        MovieTest.create_table(safe=True)
    except Exception as e:
        print(f"创建表发生异常:{e}")
    #想要对数据库里的表新增一条记录，有多种方法可以实现
    #第一种，是调用模型类的create方法，把属性值通过参数传递，直接写入一条记录
    movie_obj = MovieTest.create(rank = 1,title = '肖申克的救赎',score = 9.7,year = 1994,rating_count = 3182109)
    #因为id是自增长字段，所以调用create方法去不需要给id手动赋值，写入记录时id的值会自动被写入
    #如果打印船运模型类的create方法返回的数据类型，可以看到就是定义的模型类
    print(f"movie_obj:{type(movie_obj)}")
    #以及我们可以通过返回的实例对象的属性值，了解到写入数据库里的字段值
    #因为对象的属性值对应的是写入到表里的字段值
    print(f"id:{movie_obj.id},排名：{movie_obj.rank},标题:{movie_obj.title}")
    #需要注意的是，这里的参数名要对应数据模型类的属性名，而不是表的字段名

    movie_obj = MovieTest.create(rank=2, title='霸王别姬', score=9.6, year=1993, rating_count=2349876)
    print(f"id:{movie_obj.id},排名：{movie_obj.rank},标题:{movie_obj.title}")
    #点击MovieTest表后面的最后的这个图标按钮后，就会打开查询界面，并且它自动查询表里面所有数据后，以表格形式展示

    #因为title有唯一性，所以如果我们再次写入同样的记录，就会抛出异常

    #除了可以用模型类的create方法插入单条记录，还可以用模型类的insert方法
    #insert既可以接受一个字典数据作为参数，也可以像create方法那样通过参数赋值
    #但是在调用insert之后，它只是会返回一个ModelInsert对象，此时数据还没有被写入
    #我们还要继续调用ModelInsert 的execute方法，才是真正对数据库下达了写入指令
    #和create不同的是，这个ModelInsert 的execute方法返回的不再是模型类对象了，而是一个int类型的值
    #如果这个表有自增主键，就会返回新插入行的主键值，如果这个表没有自增主键，就会返回插入的行数（通常是1，因为插入了1行）
    movie_data3= {"rank":3,'title':"泰坦尼克号",'score':9.5,'year':1997,'rating_count':2414942}
    insert_ret = MovieTest.insert(movie_data3).execute()
    print(f"type:{type(insert_ret)} insert_ret:{insert_ret}")
    #如果前面有对rank写入重复值时，虽然由于UNIQUE的约束导致这条记录会写入失败，但是已经自增的id不会被回收，导致id这个值已经被用掉了
    #所以后续新增记录的id就会从4开始
    #另外insert除了可以接收字典作为参数外，它和create还存在的不同是：它不要求键名或参数名一定和模型类的属性名匹配
    #只要名称和表的字段名或模型类的属性名任何一个能匹配上，就可以写入记录
    insert_ret = MovieTest.insert(rank=5,title="千与千寻",score=9.4,year=2001,rating_count=2457573).execute()
    print(f"type:{type(insert_ret)} insert_ret:{insert_ret}")

    #想要一次性写入多条记录，可以调用模型类insert_many方法，它可以接受字典列表作为参数
    movie_list = [
        {"rank": 7, "title": "这个杀手不太冷", "score": 9.4, "year": 1994, "rating_count": 2490756},
        {"rank": 8, "title": "星际穿越 ", "score": 9.4, "year": 2014, "rating_count": 2092068},
        {"rank": 9, "title": "盗梦空间", "score": 9.4, "year": 2010, "rating_count": 2258027},
    ]
    result = MovieTest.insert_many(movie_list).execute()
    print(result)
    #调用insert_many之后，也别忘了调用execute方法
    #另外还要注意的是：使用insert_many方法是，字典的键名就必须和模型类的属性名一致了，否则会抛出异常
    #但是这个错误不会导致自增字段的值+1,因为还没有执行数据库操作就抛出异常而中止了
    #result对应的是批量写入记录里面第一条的id值

    #查询数据
    #如果要通过主键id字段查询对应记录，可以使用模型类get_by_id方法，这个方法会返回对应的模型对象
    movie_obj = MovieTest.get_by_id(7)
    print(f"id:{movie_obj.id},排名：{movie_obj.rank},标题:{movie_obj.title}")
    #需要注意的是，get_by_id并不是根据被命名为’id'的字段查找对应的记录，而是根据被标记为主键的字段
    #所以即使数据表没有名为id的列，也可以调用这个方法
    #如果查询一个不存在的主键，执行后程序会抛出一个MovieDoesNotExist异常，提示查询的数据不存在
    # movie_obj = MovieTest.get_by_id(20)

    #如果想查询表里面所有的记录，可以用模型类select方法，它会返回一个可迭代的ModelSelect对象，里面包含了表中所有行对应的模型对象实例
    select_result = MovieTest.select()
    print(f"共有{len(select_result)}条记录")
    #所有我们可以通过for循环，依次遍历每一个对象，打印出他们各个属性的值
    for movie_obj in select_result:
        print(f"id:{movie_obj.id},排名：{movie_obj.rank},标题:{movie_obj.title}")

    #上面我们的得到了所有的字段，也就是表里面所有列，但是如果只对排名和标题这两个字段感兴趣的话，可以在select方法中，把字段属性作为参数传入
    #这样可以限制返回的内容中只包含指定字段的值
    select_result = MovieTest.select(MovieTest.rank,MovieTest.title)
    for movie_obj in select_result:
        print(f"id:{movie_obj.id},排名：{movie_obj.rank},标题:{movie_obj.title}")
    #打印结果中可以看到只有排名和标题对应的值是有效的，其他字段的值都没有被获取到
    #在表的数据量特别大或者某些字段的内容特别长的时候，只查询指定字段可以减少返回内容的大小

    #上面都是正序输出，如果想要倒序输出的话
    #可以在调用select方法之后，可以对返回的结果继续调用order_by方法
    #然后通过参数设置某个字段排序，以及排序的方式
    select_result = MovieTest.select(MovieTest.rank, MovieTest.title).order_by(MovieTest.rank.desc())
    #比如这里传入的MovieTest.rank.desc()，表示以year字段降序排序，和desc()降序相对的是asc()
    for movie_obj in select_result:
        print(f"id:{movie_obj.id},排名：{movie_obj.rank},标题:{movie_obj.title}")

    #limit指定返回的行数
    select_result = MovieTest.select(MovieTest.rank, MovieTest.title).limit(3)
    for movie_obj in select_result:
        print(f"id:{movie_obj.id},排名：{movie_obj.rank},标题:{movie_obj.title}")

    #从指定行开始返回，用offset方法
    #offset表示跳过前n行，然后从第n+1行开始返回
    select_result = MovieTest.select(MovieTest.rank, MovieTest.title).offset(3)
    for movie_obj in select_result:
        print(f"yyid:{movie_obj.id},排名：{movie_obj.rank},标题:{movie_obj.title}")

    #结合order_by方法、limit方法、offset方法，实现类似分页查询的效果
    #比如我们想实现每页三条记录，就给order_by传入一个字段名作为排序依据，然后给limit传入参数3限制条数
    # 然后继续调用offset跳过之前分页的记录，比如第一页跳过0行，第二页跳过3行，第三页跳过6行，以此类推
    select_result = MovieTest.select().order_by(MovieTest.id).limit(3).offset(0)
    print(f"第1页共有{len(select_result)}条记录")
    for movie_obj in select_result:
        print(f"id={movie_obj.id}，排名={movie_obj.rank}，标题={movie_obj.title}，"
              f"评分={movie_obj.score}，年份={movie_obj.year}，评价人数={movie_obj.rating_count}")

    select_result = MovieTest.select().order_by(MovieTest.id).limit(3).offset(3)
    print(f"第2页共有{len(select_result)}条记录")
    for movie_obj in select_result:
        print(f"id={movie_obj.id}，排名={movie_obj.rank}，标题={movie_obj.title}，"
              f"评分={movie_obj.score}，年份={movie_obj.year}，评价人数={movie_obj.rating_count}")

    #如何用多个字段作为组合条件，实现复杂的查询
    #比如，我们怎么查询出年份在2000年之前，并且评分等于9.5或者9.6的电影记录呢
    #添加筛选条件要用到where方法，在里面传入筛选条件的表达式
    select_result = MovieTest.select().where(MovieTest.year < 2000)
    for movie_obj in select_result:
        print(f"T:{movie_obj.title} Y:{movie_obj.year}")
    #要表达评分等于9.5或9.6这个条件，除了用逻辑或连接两个等于比较之外，我们也可以用集合成员操作方法 .in_
    #它会接受一个列表作为参数，会判断值是否包含在列表中
    select_result = MovieTest.select().where(MovieTest.score.in_([9.5,9.6]))
    for movie_obj in select_result:
        print(f"T:{movie_obj.title} S:{movie_obj.score}")

    #把年份和评分的逻辑组合起来，用&进行连接，最终的结果是
    select_result = MovieTest.select().where((MovieTest.year < 2000) & (MovieTest.score.in_([9.5,9.6])))
    for movie_obj in select_result:
        print(f"TT:{movie_obj.title} Y:{movie_obj.year} S:{movie_obj.score}")

    #修改单条记录
    #对于通过查询获得的模型对象，我们可以直接修改对象里的属性值，然后调用模型对象的save方法，把属性对应的字段在数据库的表里进行更新
    #所以先通过get_by_id得到那条记录对应的数据模型对象
    movie_obj = MovieTest.get_by_id(2)
    #然后把rank属性值赋值为None
    movie_obj.rank = None
    #最后调用save方法，让改动在数据库里生效,save会返回一个整数，表示本次操作影响的行数
    result = movie_obj.save()
    print(result)

    #除了可以用模型对象的save方法对某一行进行更新，还可以用模型类的update方法，来进行批量更新
    #它可以接收关键字参数来指定要更新的字段，以及更新后的新值
    #比如我们想要把所有记录的year字段都改成2025
    # 但这样还没有结束，update方法会返回一个update对象，我们还要继续调用execute方法，才会实际执行更新操作
    result = MovieTest.update(year=2025).execute()
    #execute会返回一个整数，表示被更新的行数
    print(result)








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





