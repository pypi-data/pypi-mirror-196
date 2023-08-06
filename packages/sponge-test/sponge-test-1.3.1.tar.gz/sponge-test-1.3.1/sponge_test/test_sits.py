"""
Check the thermostat
"""
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from Xponge.analysis import MdoutReader
from sponge_test import H2O2

def setup_module():
    if os.path.exists("sits"):
        shutil.rmtree("sits")
    os.mkdir("sits")
    os.chdir('sits')

def teardown_module():
    os.chdir('..')

def test_sits():
    min_command = f"SPONGE -mode minimization -step_limit 10000 -default_in_file_prefix {H2O2.prefix} \
                   -LJ_in_file no_lj.txt -charge_in_file no_charge.txt -cv_in_file cv.txt \
                   -cutoff 1 -skin 1 -neighbor_list_refresh_interval 100000 -dihedral_in_file my_dihedral.txt"
    run_command = f"SPONGE -mode NVT -dt 1e-3 -default_in_file_prefix {H2O2.prefix} \
                   -LJ_in_file no_lj.txt -charge_in_file no_charge.txt -cv_in_file cv.txt \
                   -cutoff 1 -skin 1 -neighbor_list_refresh_interval 100000 -dihedral_in_file my_dihedral.txt \
                   -thermostat middle_langevin -coordinate_in_file restart_coordinate.txt -write_information_interval 100 -sits_dihedral_in_file my_sits_dihedral.txt"

    with open("no_charge.txt", "w") as f:
        f.write("4\n0\n0\n0\n0\n")
    with open("no_lj.txt", "w") as f:
        f.write("4 1\n0\n\n0\n\n0\n0\n0\n0\n")
    with open("my_dihedral.txt", "w") as f:
        f.write("2\n2 0 1 3 2 15 0.4\n2 0 1 3 3 5 -0.6\n")
    with open("my_sits_dihedral.txt", "w") as f:
        f.write("2\n2 0 1 3 2 15 0.4\n2 0 1 3 3 5 -0.6\n")
    with open("cv.txt", "w") as f:
        f.write("""torsion
{
CV_type = dihedral
atom = 2 0 1 3
}

print_CV = torsion
""")
    assert os.system(min_command) == 0
    assert os.system(run_command + " -SITS_mode observation -SITS_atom_numbers 4 -step_limit 20000") == 0
    assert os.system(run_command + " -SITS_mode iteration  -SITS_atom_numbers 4 \
-SITS_T_low 100 -SITS_T_high 6000 -SITS_k_numbers 6000 -SITS_pe_b -0.0 -step_limit 100000") == 0
    assert os.system(run_command + " -SITS_mode production  -SITS_atom_numbers 4 \
-SITS_T_low 100 -SITS_T_high 6000 -SITS_k_numbers 6000 -SITS_pe_b -0.0 -SITS_nk_in_file SITS_nk_rest.txt -step_limit 980000") == 0
    t = MdoutReader("mdout.txt")
    bias = t.SITS_bias
    t = t.torsion
    kT = -8.314 * 300 / 4184
    w = np.exp(-bias/kT)
    t = np.concatenate((t, t + np.pi * 2, t - np.pi * 2))
    w = np.concatenate((w, w, w))
    kernel = gaussian_kde(t, weights=w, bw_method=0.01)
    positions = np.linspace(-np.pi, np.pi, 300)
    result = kernel(positions)
    result = -8.314 * 300 / 4184 * np.log(result)
    result -= min(result)
    theory = 0.3 * np.cos(2 * positions - 0.4) + 0.1 * np.cos(3 * positions + 0.6)
    theory *= 50
    theory -= min(theory)
    plt.plot(positions, result, label="simulated results")
    plt.plot(positions, theory, label="potential")
    plt.legend()
    plt.savefig("sits.png")
    plt.clf()
