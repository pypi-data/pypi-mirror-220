"""
python v3.9.0
@Project: hotpot
@File   : test_gaussian
@Auther : Zhiyuan Zhang
@Data   : 2023/7/19
@Time   : 7:33
"""
import unittest as ut
import hotpot as hp
import hotpot.tanks.qm.gaussian as gs


class TestOptions(ut.TestCase):

    def test_options(self):
        """"""
        ops = gs._Options()
        route = ops.route
        output = route.opt.ONIOM.Micro()

        return output


if __name__ == "__main__":
    test = TestOptions()
    test.test_options()
