from rotest.core.block import TestBlock
from rotest.core.flow import TestFlow


class MyBlock(TestBlock):
    def test_method(self):
        pass


class HappyFlow(TestFlow):
    blocks = [MyBlock] * 100
