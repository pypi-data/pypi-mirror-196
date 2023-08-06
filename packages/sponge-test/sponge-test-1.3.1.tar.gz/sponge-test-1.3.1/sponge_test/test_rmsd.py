import os
import shutil
import MDAnalysis as mda
import Xponge.analysis.md_analysis as xmda #pylint: disable=unused-import
from Xponge.analysis import MdoutReader
from MDAnalysis.analysis import rms
import numpy as np
from sponge_test import dipeptide

def setup_module():
    if os.path.exists("rmsd"):
        shutil.rmtree("rmsd")
    os.mkdir("rmsd")
    os.chdir('rmsd')

def teardown_module():
    os.chdir('..')

def test_rmsd():
    assert os.system(f"Xponge maskgen -p {dipeptide.prefix + '.mol2'} \
    -o rmsd_atom.txt -oc rmsd_coordinate.txt -s \"not resname WAT\"") == 0
    with open("cv.txt", "w") as f:
        f.write("""RMSD
{
    CV_type = rmsd
    atom_in_file = rmsd_atom.txt
    coordinate_in_file = rmsd_coordinate.txt
}

print_CV = RMSD

restrain
{
    CV = RMSD
    weight = 1
    reference = 0
}
""")
    assert os.system(f"SPONGE -default_in_file_prefix {dipeptide.prefix} -dt 2e-3 \
-mode NPT -thermostat middle_langevin -barostat andersen_barostat \
-cv_in_file cv.txt -step_limit 10000 -write_information_interval 1000 -constrain_mode SHAKE") == 0
    u = mda.Universe(f"{dipeptide.prefix + '.mol2'}", "mdcrd.dat", box="mdbox.txt")
    u2 = mda.Universe(f"{dipeptide.prefix + '.mol2'}")
    r = rms.RMSD(u, u2, select = "not resname WAT")
    r.run()
    t = MdoutReader("mdout.txt").RMSD - r.results.rmsd[:,2]
    print(t)
    assert np.all(np.abs(t) < 0.01)
