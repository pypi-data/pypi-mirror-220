# -*- coding: utf-8 -*-
import sys

sys.path.append("..")

from dspawpy.io.structure import _from_pdb

ss = _from_pdb("ala_phe_ala.pdb")
print(len(ss))
print(ss[0])

from dspawpy.io.write import to_file

to_file(ss[0], "POSCAR")
