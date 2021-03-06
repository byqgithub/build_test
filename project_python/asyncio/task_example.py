import asyncio
import time


async def compute(x, y):
    print("Compute {} + {}...".format(x, y))
    await asyncio.sleep(2.0)
    return x+y


async def print_sum(x, y):
    result = await compute(x, y)
    print("{} + {} = {}".format(x, y, result))
    return result


async def main():
    start = time.time()
    result = await asyncio.wait([print_sum(0, 0), print_sum(1, 1), print_sum(2, 2)])
    print(result)
    print("Total elapsed time {}".format(time.time() - start))


# async def factorial(name, number):
#     f = 1
#     for i in range(2, number + 1):
#         print(f"Task {name}: Compute factorial({i})...")
#         await asyncio.sleep(1)
#         f *= i
#     print(f"Task {name}: factorial({number}) = {f}")
#     return f
#
#
# async def main():
#     # 并发运行三个任务
#     result = await asyncio.gather(
#         factorial("A", 5),
#         factorial("B", 3),
#         factorial("C", 4),
#     )
#     print(result)
#
asyncio.run(main())
