import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from src.utils.singleton import singleton


@singleton
class DummyClass:
    def __init__(self, value):
        self.value = value


def test_singleton():
    instance1 = DummyClass(10)
    instance2 = DummyClass(20)

    assert instance1 is instance2
    assert instance1.value == 10
    assert instance2.value != 20
