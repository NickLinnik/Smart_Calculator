from unittest import TestCase

import main


class Test(TestCase):
    def test_main(self):
        self.assertEqual(main.solve('2 + 3 -1 + vara', vara=10), 14)
        self.assertEqual(main.solve('2 +- - 3 ++---1 + vara', vara=10), 14)
        self.assertEqual(main.solve('a + b ^ (1/3)', a=7, b=27), 10)
        self.assertEqual(main.solve('-2 ^ (-((3 -2)^   10 )*-2 )'), 4)
