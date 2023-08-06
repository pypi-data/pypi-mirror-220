"""
Test for client module
"""
import pytest
from mock import MockCall, MockLoopingCall

import mbsim.core.client as mb

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.parametrize("loop", [True, False])
def testStart(monkeypatch, loop):
    """
    Test client Start function
    """
    genloop = MockLoopingCall(lambda: None)
    starttasks = MockCall()

    monkeypatch.setattr(mb, "getloop", lambda: genloop)
    monkeypatch.setattr(mb.Task, "startTasks", starttasks)

    if loop:
        mb.start(loop=genloop)
    else:
        mb.start()

    assert starttasks.count == 1
    assert genloop.forever


def testStop(monkeypatch):
    """
    Test client Stop function
    """
    ml = MockLoopingCall(lambda: None)
    mc = MockCall()
    monkeypatch.setattr(mb.Task, "loop", ml)
    monkeypatch.setattr(mb.Task, "stopTasks", mc)

    mb.stop()

    assert mc.count == 1
    assert ml.stopped
