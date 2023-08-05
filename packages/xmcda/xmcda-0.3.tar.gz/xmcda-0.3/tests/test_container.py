from xmcda.container import Container

from .utils import XMCDATestCase


class E:
    def __init__(self, id):
        self.id = id


class TestContainer(XMCDATestCase):

    def test_remove(self):

        c = Container()
        e1, e2 = E('1'), E('2')
        c.append(e1)
        c.append(e2)
        self.assertRaises(ValueError, c.remove, None)
        self.assertRaises(ValueError, c.remove, 'unknown id')

        c.remove('2')
        self.assertSequenceEqual(c, [e1])

        c.remove(e1)
        self.assertSequenceEqual(c, [])

    def test_contains(self):
        c = Container()
        e1, e2 = E('1'), E('2')
        self.assertFalse(e1 in c)
        self.assertFalse("1" in c)
        self.assertFalse(1 in c)

        c.append(e1)
        c.append(e2)
        for e in e1, e2:
            self.assertTrue(e in c)
            self.assertTrue(e.id in c)

        self.assertFalse(E('1') in c)
