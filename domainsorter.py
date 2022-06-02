import asyncio
import time
from collections import defaultdict
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import DefaultDict

import aiofiles
import easygui
import uvloop
from tqdm import tqdm


async def main():
    filelines = fileread(filenameis)
    tasks = []
    async for email in filelines:
        tasks.append(asyncio.create_task(worker(email)))

    await asyncio.gather(*tasks)
    for domain in domainsset:
        async with aiofiles.open(f"sorteddomains/{domain}.txt", "a+") as f:
            await f.writelines(domainsset[domain])


async def worker(email: str):
    '''This worker func does all the work that im wanting to do'''
    async with workerslimit:
        temp = await checkifstrcontains(email)
        if temp:
            try:
                domain = email.split(":", 1)[0].split("@", 1)[-1]
                domainsset[domain].add(f"{email}\n")
            except Exception as e:
                # pass
                print(f"{email.casefold()}:{e}")
        pbar.update()


async def fileread(filenameis: str) -> AsyncGenerator[str, None]:
    """
        Lazy function to read a file line by line into a generator object,
        Takes in a filename and returns an async generator object.
    """
    async with aiofiles.open(filenameis, "r", errors='backslashreplace') as f:
        async for line in f:
            yield line.strip()


async def checkifstrcontains(email: str) -> bool:
    return "@" in email


def ncounter(filenameis: str) -> int:
    ncounter: int = 0
    with open(filenameis, "r", errors='backslashreplace') as f:
        for _ in f:
            ncounter += 1
    return ncounter


async def fileread(filenameis: str) -> AsyncGenerator[str, None]:
    """
        Lazy function to read a file line by line into a generator object,
        Takes in a filename and returns an async generator object.
    """
    async with aiofiles.open(filenameis, "r", errors='backslashreplace') as f:
        async for line in f:
            yield line.strip()


async def checkifstrcontains(email: str) -> bool:
    return "@" in email


def ncounter(filenameis: str) -> int:
    """
    Count all the lines in a file and return an int: ncounter(int) is number of lines in files
    """
    ncounter: int = 0
    with open(filenameis, "r", errors='backslashreplace') as f:
        for _ in f:
            ncounter += 1
    return ncounter


if __name__ == "__main__":
    uvloop.install()
    startTime = time.time()
    Path("sorteddomains").mkdir(exist_ok=True)
    workerslimit = asyncio.Semaphore(100)
    domainsset: DefaultDict[str, set[str]] = defaultdict(set)
    filenameis = easygui.fileopenbox(msg="Choose a file", )

    pbar = tqdm(total=ncounter(filenameis))
    asyncio.run(main())
    executionTime = time.time() - startTime
    print("Execution time in seconds: " + str(executionTime))
    pbar.close()
