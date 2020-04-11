from threading import Thread
import asyncio
import time


async def sleep(second):
    print("sleep %s second \n" % second)
    await asyncio.sleep(second)


async def hello(sequence):
    print("hello %s \n" % sequence)
    await sleep(sequence)
    # return sequence


async def main():
    tasks = [asyncio.create_task(hello(i)) for i in range(5)]
    await asyncio.gather(*tasks)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


def more_work(x):
    print('More work {}'.format(x))
    time.sleep(x)
    print('Finished more work {}'.format(x))


# 在主线程创建事件循环，并在另一个线程中启动
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()

# 在主线程中注册回调函数，在子线程中按顺序执行回调函数
# new_loop.call_soon_threadsafe(more_work, 1)
# new_loop.call_soon_threadsafe(more_work, 3)

# 在主线程中注册回调协程函数，在子线程中按异步执行回调函数
asyncio.run_coroutine_threadsafe(hello(6), new_loop)
asyncio.run_coroutine_threadsafe(hello(7), new_loop)

# 不会阻塞主线程
for i in range(10):
    print(i)
t.join()
