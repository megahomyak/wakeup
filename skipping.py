import asyncio

class Skip:
    def __await__(self):
        yield

SKIPPING = True

async def a():
    while True:
        print(123)
        if SKIPPING:
            await Skip()

async def b():
    while True:
        print(456)
        await Skip()

async def main():
    await asyncio.gather(a(), b())

asyncio.run(main())
