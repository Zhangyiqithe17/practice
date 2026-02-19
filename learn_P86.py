#怎么把数据高效地爬下来
#单个CPU一次只能执行一个线程的指令流，但操作系统可以让不同线程之间快速切换，每秒钟可以达到上万次，给用户所有线程都在并发运行的感觉

#python标准库里提供了一个叫threading的模块，可以帮我们创建和管理线程，不需要额外安装，所以可以直接进行导入
import threading
#treading模块里有一个Thread类，我们调用这个类的构造函数，就可以创建出一个线程对象，我们实例化Thread对象时可以传递多个参数
    #其中两个最常用的是target和args，参数target的值是像函数这种的可调用对象，代表线程启动后要执行的任务
    #也就是说线程启动后会调用target参数指向的那个可调用对象
    # args参数的值必须是元组类型，包含要传递给target参数指向的那个可调用对象的参数值
        #如果那个参数值接收多个参数，我们就要把多个参数所对应的值按顺序放入到元组里

import time
import threading
# from symbol import with_stmt
from concurrent.futures import ThreadPoolExecutor

balance = 1000
# def deliver_parcel(parcel_id):
#     print(f"快递{parcel_id}:开始派送")
#     time.sleep(2)
#     print(f"快递{parcel_id}:派送完成")
#     reduce_balance()

#假如加入奖金计算机制：送完一个快递，快递原可以拿10元奖金，一共1000元奖金，快递员每送完一次快递并拿取奖金时，应该及时更新数据
#我们可以创建一个全局变量balance来表示余额，以及创建一个reduce_balance函数
# def reduce_balance():
#     global balance #声明我们要在函数里修改balance这个全局变量，因为函数里的变量默认视为局部变量，如果不加，最后一行对balance的复制会被视为是创建局部变量
#     previous_balance = balance
#     time.sleep(0.1)
#     balance = previous_balance - 10

# thread1 = threading.Thread(target=deliver_parcel, args=(1,),name="张三")
#
# #比如上面这个代码里，我们给Thread构造函数的target，设置为deliver_parcel这个函数，表示线程任务是调用deliver_parcel函数
# # 然后给args设置为包含一个整数1的元祖，表示线程在调用deliver_parcel时会传入1作为参数值
# #现在我们给主线程创建一条子线程作为帮手，那还可以尝试创建更多出来
# thread2 = threading.Thread(target=deliver_parcel, args=(2,),name="李四")
# thread3 = threading.Thread(target=deliver_parcel, args=(3,),name="王五")
# #实例化3个Thread对象，目标是让每一个子线程都去负责一个快递的派送，把任务时长缩到更短
# #但这个时候，每个线程还不会开始执行，我们还需要调用Thread对象的start方法，来启动线程活动
# #并且为了能计算出整体缩耗费的时间，我们用了time模块的time方法记录下开始时间和结束时间
# #那么主线程，也就是执行这个Python程序的线程，会负责执行子线程的start、打印耗时语句等等
# #而子线程会分别执行deliver_parcel
# start = time.time()
# thread1.start()
# thread2.start()
# thread3.start()
# # print(f"总耗时：{time.time()-start:.2f}秒")
#
# #到这里，运行结果并不尽人意，如果多运行几遍，每次打印出来的结果还不一样，而且总耗时2秒是不对的，因为一个快递最少也要2秒
# #这说明总耗时的计算发生在了那三个调用deliver_parcel的线程执行完成之前，主线程在调用start后并没有等待子线程执行完毕，就继续执行打印语句了
# #而且虽然线程启动的顺序是1、2、3，但是完成的顺序是1、3、2，这也是多线程的特点：每个线程由操作系统调度，执行顺序是不可预测的
#
# #我们需要调用Thread对象的join方法，用在阻塞主线程，直到被调用join方法的线程执行结束
# thread1.join()
# # print(f"收到{thread1.name}的完成通知")
# thread2.join()
# # print(f"收到{thread2.name}的完成通知")
# thread3.join()
# # print(f"收到{thread3.name}的完成通知")
# print(f"余额:{balance}")
# print(f"总耗时：{time.time()-start:.2f}秒")
#当线程A调用线程B的join方法时，线程A会进入阻塞状态，也就是暂停执行，直到线程B完全执行结束，线程A才会继续执行
#我们也可以在join后面执行一条打印语句，只要能运行到后面的print，说明前面的join已经不再阻塞主线程了
#每个Thread对象都有一个表示名称的name属性，所以我们可以把name一起打印出来
#现在打印出来的总耗时就是合理的了，数字也从单线程时的6秒缩短到了2秒

#这种系统默认分配的名字不方便我们记忆和辨别，所以也可以给线程设置自定义的名字
#具体在：我们可以实例化Thread对象的时候。增加一个name参数，给各个线程增加一个好记忆的名字

#但是到现在，打印结果里面还会出现一些莫名其妙消失的换行和多出来的空白行
#这是因为出现了线程竞争（多个线程同时访问和操作共享资源，比如变量、文件、数据库等等，导致最终结果依赖于线程执行的顺序，从而让结果变得不可预测）

#在这个例子里，多个线程会同时调用print函数而产生线程竞争
#而且print并不是原子操作，原子操作指的是不可分割的操作，但是print实际的执行步骤拆分出了多步，包括构建字符串、写入字符串到缓冲区、写入换行符到缓冲区、输出到终端
    #这里的缓冲区就属于线程之间的共享资源，因为只有一个缓存区用于暂存要输出到终端的内容，那么当多个线程在差不多的时间调用print函数的时候
    #每个print内部的多个步骤会交替进行，从而导致缓存区可能同时暂存了不同print写入的字符串
    #然后混合了多个线程写入的字符串，会在某个print执行刷新缓冲区这个步骤的时候，输出到终端，导致我们看到的混乱且不可预测的打印结果

#所以，因为print不具备原子性，它是非线程安全的
#当竞争发生在共享变量的修改上时，会导致更严重的后果，比如可能造成数据损坏，程序状态不一致等难以追踪的逻辑错误，让最终值完全偏离预期

#打印结果本来应该是970，却显示是990，结果错误
#再试一下把业务规模扩大，让10个快递小哥同时出发，也就是通过for循环创建10条子线程出来，并且依次调用各个Thread对象的start和join


#即使扩大到了10个快递员，余额还是990，这是因为reduce_balance函数和前面的print一样，并不是原子操作，执行过程中的中间步骤会被其他线程打断
#如果要解决这个问题，需要让reduce_balance的执行不会被中途打断，我们可以给它加一把锁
#锁的概念是：同一时间只有一个线程可以获得锁，其他线程就要等着，直到这个锁被释放
#那么我们就可以给对共享资源的操作，加上一把锁进行保护
#当线程1想操作记账本的时候，他必须先获得锁，而此时其他线程因为没有拿到锁，必须等待，直到线程1完成操作后把锁释放
    #释放的时候，其他被锁阻塞的线程都可以去竞争，但最终也只会有一个线程获得锁，确保共享资源不会被多个线程同时修改
#Threading里有一个叫lock的类，所以我们可以调用lock构造函数实例化一个锁，来保护对balance变量的访问操作
balance_lock = threading.Lock()
#上锁的方法也很简单：with后面跟上锁名，冒号，然后我们把需要避免线程竞争语句，全部放在下面的代码块里
#除了reduce_balance函数，我们前面还遇到了打印混乱的问题，所以我们可以给print函数也加上锁，同样的方法实例化一个Lock对象
print_lock = threading.Lock()
def deliver_parcel(parcel_id):
    with print_lock:
        print(f"快递{parcel_id}:开始派送")
    time.sleep(2)
    with print_lock:
        print(f"快递{parcel_id}:派送完成")
    # reduce_balance()
    return parcel_id,time.time()-start

def reduce_balance():
    global balance
    #with语句会自动管理锁的生命周期，进入with块时自动获取锁，退出with块时自动释放锁
    #所以可以避免写代码时忘记调用锁的释放方法
    with balance_lock:
        previous_balance = balance
        time.sleep(0.1)
        balance = previous_balance - 10

start = time.time()
future_list = []
# thread_list = []
# for i in range(10):
#     thread = threading.Thread(target=deliver_parcel, args=((i+1),))
#     thread_list.append(thread)
#     thread.start()
#
# for thread in thread_list:
#     thread.join()



#因为上了锁，所以reduce_balance函数里面，上了balance_lock锁里面，0.1秒等待过程中，锁并没有别被释放，剩下需要执行reduce_balance的线程拿不到锁
#于是也处于被阻塞的状态
#所以也提醒我们，要对不同的共享资源合理分配不同的锁，比如print的锁和reduce_balance的锁不应该是同一个，不然线程之间对锁的竞争会造成更多阻塞时间
#除此之外，线程的创建和销毁也会带来一定的开销，所以后面我们会了解线程池的概念

#每个线程的创建和销毁都要消耗系统资源，比如CPU、内存等，也会增加额外的时间，所以我们最好尽可能避免频繁创建和销毁线程，最好是能复用已有线程
#线程池就是用来解决这个问题的，并且可以实现线程的高效管理
#为了能创建一个线程池，我们要导入ThreadPoolExecutor类，它在concurrent.futures模块下，它也是Python标准库的内置模块，不需额外安装
# from concurrent.futures import ThreadPoolExecutor
#调用ThreadPoolExecutor类的构造函数，我们可以创建出一个线程池对象，但是更常用的是结合with块，可以实现线程池资源的自动管理
#线程池中最多包含的子线程数是由ThreadPoolExecutor的max_workers参数决定的
#比如我们希望线程池里最多创建出3个子线程，就设置这个参数值为3，但是这不代表线程池会在一开始就一次性创建出那么多个子线程
#而是会在执行任务时，根据任务数量自动增加子线程，直到达到max_workers这个上限为止
#创建的线程数达到上限之后，任务再过来时线程池就不会再创建新线程了，新任务会进入队列等待，直到某个已创建的线程变得空闲，然后那个线程再去执行新任务
#使用线程池的话，我们就不需要手动单独创建Thread对象，和我们就不需要手动单独创建Thread对象，和安排各个线程的任务了
#而是调用线程池对象的submit方法，向线程池提交任务
#如果用线程池，原先的逻辑不需要做太多改动，只需要改中间创建线程，和等待线程执行完成的逻辑

with ThreadPoolExecutor(max_workers=5) as pool:
    for i in range(10):
        future = pool.submit(deliver_parcel, i+1)
        future_list.append(future)
    print("全部任务已提交")
#上面调用了pool的submit方法向线程池提交任务，第一个参数同样是比如函数这种可调用对象，如果可调用对象也有需要接收的参数的话，我们从第二个参数开始依次按顺序传入参数值
#任务提交之后，线程池会自动分配空闲线程去处理任务，线程会等待线程池分配新的任务

# print(f"余额:{balance}")
print(f"总耗时：{time.time() - start:.2f}秒")
#从打印结果可以看出，我们调用submit方法提交送快递的任务后，立刻有三个线程开始执行，任务完成后，这三个线程又会继续去完成被安排的后续任务
    #直到我们向线程池提交的所有任务都被执行完成
    #另外，虽然我们没有让主线程去等待子线程执行完成，但是总耗时的计算和输出也是没有问题的
    #这是因为用线程池结合with代码块进行管理的时候，线程池会自动等待所有已提交任务的完成，不需要显式调用各个线程的join方法
    #在退出with代码块时，线程池也会自动释放所有资源

#有些时候除了某些特定任务的执行，也需要获得任务执行后返回的结果，比如，我们可以给deliver_parcel函数新增一个return语句
    #把派送的快递ID以及主线程计时开始到派送完成所消耗的时长进行返回

#那么线程里要怎么获取到函数返回的结果呢？
    #submit方法会返回一个Future对象，这个对象里会保存任务执行结果，包括可调用对象的返回值
    #我们可以新增一个储存放回的Future对象的列表，然后当线程池里的所有任务都执行完成后，循环列表里的各个对象
    #要获得任务的返回结果，我们可以调用Future对象result方法，得到函数返回值
for future in future_list:
    print(f"任务返回值:{future.result()}")

#result方法同样造成线程等待，因为result会让调用线程暂停执行，直到获取到任务结果
    #但是在现在代码里，因为调用result的时候所有任务都完成了，所以没有消耗额外的等待时间
