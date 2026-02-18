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

def deliver_parcel(parcel_id):
    print(f"快递{parcel_id}:开始派送")
    time.sleep(2)
    print(f"快递{parcel_id}:派送完成")

thread1 = threading.Thread(target=deliver_parcel, args=(1,))

#比如上面这个代码里，我们给Thread构造函数的target，设置为deliver_parcel这个函数，表示线程任务是调用deliver_parcel函数
# 然后给args设置为包含一个整数1的元祖，表示线程在调用deliver_parcel时会传入1作为参数值
#现在我们给主线程创建一条子线程作为帮手，那还可以尝试创建更多出来
thread2 = threading.Thread(target=deliver_parcel, args=(2,))
thread3 = threading.Thread(target=deliver_parcel, args=(3,))
#实例化3个Thread对象，目标是让每一个子线程都去负责一个快递的派送，把任务时长缩到更短
#但这个时候，每个线程还不会开始执行，我们还需要调用Thread对象的start方法，来启动线程活动
#并且为了能计算出整体缩耗费的时间，我们用了time模块的time方法记录下开始时间和结束时间
#那么主线程，也就是执行这个Python程序的线程，会负责执行子线程的start、打印耗时语句等等
#而子线程会分别执行deliver_parcel
start = time.time()
thread1.start()
thread2.start()
thread3.start()
# print(f"总耗时：{time.time()-start:.2f}秒")

#到这里，运行结果并不尽人意，如果多运行几遍，每次打印出来的结果还不一样，而且总耗时2秒是不对的，因为一个快递最少也要2秒
#这说明总耗时的计算发生在了那三个调用deliver_parcel的线程执行完成之前，主线程在调用start后并没有等待子线程执行完毕，就继续执行打印语句了
#而且虽然线程启动的顺序是1、2、3，但是完成的顺序是1、3、2，这也是多线程的特点：每个线程由操作系统调度，执行顺序是不可预测的

#我们需要调用Thread对象的join方法，用在阻塞主线程，直到被调用join方法的线程执行结束
thread1.join()
print(f"收到{thread1.name}的完成通知")
thread2.join()
print(f"收到{thread2.name}的完成通知")
thread3.join()
print(f"收到{thread3.name}的完成通知")
print(f"总耗时：{time.time()-start:.2f}秒")
#当线程A调用线程B的join方法时，线程A会进入阻塞状态，也就是暂停执行，直到线程B完全执行结束，线程A才会继续执行
#我们也可以在join后面执行一条打印语句，只要能运行到后面的print，说明前面的join已经不再阻塞主线程了
#每个Thread对象都有一个表示名称的name属性，所以我们可以把name一起打印出来
#现在打印出来的总耗时就是合理的了，数字也从单线程时的6秒缩短到了2秒