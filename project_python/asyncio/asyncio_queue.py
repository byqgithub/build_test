import asyncio
import itertools as it
import os
import random
import time


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


async def randint(a: int, b: int) -> int:
    return random.randint(a, b)


async def randsleep(a: int = 1, b: int = 5, caller=None) -> None:
    i = await randint(a, b)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue) -> None:
    """生产者"""
    n = await randint(1, 5)
    for _ in it.repeat(None, n):  # 同步添加任务
        await randsleep(caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to queue.")


async def consume(name: int, q: asyncio.Queue) -> None:
    """消费者"""
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}>"
              f" in {now - t:0.5f} seconds.")
        q.task_done()


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    # asyncio.run()会自动运行消费者和生产者
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    await asyncio.gather(*producers) # 等待生产者结束
    await q.join()  # 阻塞直到队列中的所有项目都被接收和处理
    # 取消消费者
    for c in consumers:
        c.cancel()


if __name__ == "__main__":
    random.seed(444)
    start = time.perf_counter()
    asyncio.run(main(2, 3))
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")