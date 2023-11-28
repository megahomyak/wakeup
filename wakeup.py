import asyncio

class _Sleeper:
    def __await__(self):
        yield self

def sleep():
    return _Sleeper()

class _skip:
    def __await__(self):
        yield

class WakeupLoop:
    def __init__(self):
        self._active_tasks = {}
        self._sleeping_tasks = {}

    def add_task(self, key, coroutine):
        self._active_tasks[key] = coroutine

    def wake_up(self, key):
        coroutine = self._sleeping_tasks.pop(key)
        self._active_tasks[key] = coroutine

    async def run(self):
        while True:
            new_active_tasks = {}
            while self._active_tasks:
                key, task = self._active_tasks.popitem()
                result = task.send(None)
                if isinstance(result, _Sleeper):
                    self._sleeping_tasks[key] = task
                else:
                    new_active_tasks[key] = task
            self._active_tasks = new_active_tasks
            await _skip()

async def test():
    loop = WakeupLoop()

    async def task(name):
        while True:
            await asyncio.sleep(0.5)
            print(name)
            await sleep()

    loop.add_task(1, task(1))
    loop.add_task(2, task(2))
    loop.add_task(3, task(3))

    async def waker():
        await asyncio.sleep(2)
        loop.wake_up(1)
        await asyncio.sleep(2)
        loop.wake_up(2)
        await asyncio.sleep(2)
        loop.wake_up(3)
        loop.wake_up(1)
        await asyncio.sleep(2)
        loop.wake_up(2)

    await asyncio.gather(loop.run(), waker())

asyncio.run(test())
