class Sleeper

def _skip():


class WakeupLoop:
    def __init__(self):
        self._active_tasks = {}
        self._inactive_tasks = {}

    def add_task(self, key, coroutine):
        self._active_tasks[key] = coroutine

    async def run(self):
        while True:
            await
