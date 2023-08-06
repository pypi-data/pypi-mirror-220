"""
python v3.9.0
@Project: hotpot
@File   : test_cheminfo
@Auther : Zhiyuan Zhang
@Data   : 2023/7/16
@Time   : 22:21
Notes:
    Test `hotpot/cheminfo` module
"""
import unittest as ut
import hotpot as hp


class TestMolecule(ut.TestCase):
    """ Test `hotpot/cheminfo/Molecule` class """
    def test_read_from(self):
        """ test the `read_from` method """
        mol_ab16log = hp.Molecule.read_from('examples/struct/abnormal_output.log', 'g16log', force=True)
        return mol_ab16log


if __name__ == '__main__':
    test_mol = TestMolecule()
    mol = test_mol.test_read_from()
