"""
Test for tasks module
"""
import asyncio

import pytest
from mock import MockCall, MockLoopingCall

from mbsim.core.tasks import Task, getloop

pytest_plugins = ("pytest_asyncio",)


class TestGetLoop(object):
    """
    This test the getloop function
    """

    def raiseRintime(self):
        raise RuntimeError

    def test_new_event_loop(self, monkeypatch):
        """
        Test if new event loop is passed
        """
        monkeypatch.setattr(asyncio, "get_running_loop", self.raiseRintime)
        loop = getloop()
        assert isinstance(loop, asyncio.BaseEventLoop)

    @pytest.mark.asyncio
    async def test_running_loop(self, event_loop):
        """
        Test running loop is passed
        """
        loop = getloop()
        assert loop is event_loop


class Test_Tasks(object):
    """
    Group of test to test Tasks
    """

    @pytest.mark.parametrize(
        "inter,args,kwargs,now,func",
        [
            (1, (), {}, False, print),
            (2, ("Hello"), {}, False, dict),
            (3, (), {"Hello": "World"}, False, set),
            (4, (), None, True, max),
        ],
    )
    def test_createDecorator(self, inter, args, kwargs, now, func, monkeypatch):
        """
        test the creation of tasks
        """
        Task(inter, args=args, kwargs=kwargs, now=now)(func)
        assert func is Task.tasks[-1].func
        assert inter is Task.tasks[-1].inter
        assert args is Task.tasks[-1].args
        assert now is Task.tasks[-1].now
        if kwargs is None:
            assert isinstance(Task.tasks[-1].kwargs, dict)
        else:
            assert kwargs is Task.tasks[-1].kwargs

    @pytest.mark.parametrize(
        "inter,args,kwargs,now,func",
        [
            (1, (), {}, False, print),
            (2, ("Hello"), {}, False, dict),
            (3, (), {"Hello": "World"}, False, set),
            (4, (), None, True, max),
        ],
    )
    def test_createInstance(self, inter, args, kwargs, now, func, monkeypatch):
        """
        test the creation of tasks
        """
        Task(inter, func=func, args=args, kwargs=kwargs, now=now)
        assert func is Task.tasks[-1].func
        assert inter is Task.tasks[-1].inter
        assert args is Task.tasks[-1].args
        assert now is Task.tasks[-1].now
        if kwargs is None:
            assert isinstance(Task.tasks[-1].kwargs, dict)
        else:
            assert kwargs is Task.tasks[-1].kwargs

    @pytest.mark.parametrize(
        "tasks",
        [[], [MockLoopingCall(lambda: None)], [MockLoopingCall(lambda: None) for _ in range(3)]],
    )
    def test_startTasks(self, tasks, monkeypatch):
        """
        Test class method and by proxy instance start method
        """
        monkeypatch.setattr(Task, "tasks", tasks)
        Task.startTasks()
        for task in Task.tasks:
            assert task.started

    @pytest.mark.parametrize(
        "tasks",
        [[], [MockLoopingCall(lambda: None)], [MockLoopingCall(lambda: None) for _ in range(3)]],
    )
    def test_stopTasks(self, tasks, monkeypatch):
        """
        Test class method and by proxy instance stop method
        """
        monkeypatch.setattr(Task, "tasks", tasks)
        Task.stopTasks()
        for task in Task.tasks:
            assert task.stopped

    def test_startTask(self, monkeypatch):
        """
        Test starting a task
        """
        loop = MockLoopingCall(lambda: None)
        monkeypatch.setattr(Task, "loop", loop)
        task = Task(1, func=print)
        monkeypatch.setattr(task, "wrap", MockCall())
        task.start()
        assert loop.started

    def test_stopTask(self, monkeypatch):
        """
        Test stopping a task
        """
        mtask = MockLoopingCall(lambda: None)
        task = Task(1, func=print)
        monkeypatch.setattr(task, "task", mtask)
        task.stop()
        assert mtask.stopped

    @pytest.mark.parametrize("block", [True, False])
    @pytest.mark.parametrize("now", [True, False])
    @pytest.mark.asyncio
    async def test_funcwrap(self, event_loop, now, block, monkeypatch):
        """
        Test wrap function for async Call passing args
        """
        mc = MockCall()
        monkeypatch.setattr(Task, "loop", event_loop)
        task = Task(0.3, func=mc, now=now, block=block)
        test = event_loop.create_task(task.wrap(a=("hello",), kw={"a": 1}))
        await asyncio.sleep(0.4)
        test.cancel()
        if now:
            assert mc.count == 2
        else:
            assert mc.count == 1
        for val in mc.args:
            assert val[0] == "hello"
        for val in mc.kwargs:
            assert val == {"a": 1}

    @pytest.mark.asyncio
    async def test_blockcoroutine(self, event_loop, monkeypatch):
        """
        Test that giving task a coroutine and set blocking true
        """
        with pytest.raises(ValueError, match="{} cannot be blocking if is coroutine".format(asyncio.sleep.__name__)):
            monkeypatch.setattr(Task, "loop", event_loop)
            task = Task(1, func=asyncio.sleep, args=(1,), block=True)
            task.start()
            await task.task

    @pytest.mark.parametrize("now", (True, False))
    @pytest.mark.asyncio
    async def test_asyncwrap(self, event_loop, now, monkeypatch):
        """
        Test if a coroutine is passed to task
        """

        async def test(mc):
            """Mock coroutine"""
            mc()

        mc = MockCall()
        monkeypatch.setattr(Task, "loop", event_loop)
        task = Task(0.3, func=test, now=now)
        test = event_loop.create_task(task.wrap(a=(mc,), kw={}))
        await asyncio.sleep(0.4)
        if now:
            assert mc.count == 2
        else:
            assert mc.count == 1
