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
    if os.path.exists("meta1d"):
        shutil.rmtree("meta1d")
    os.mkdir("meta1d")
    os.chdir('meta1d')

def teardown_module():
    os.chdir('..')

def test_meta1d():
    min_command = f"SPONGE -mode minimization -step_limit 10000 -default_in_file_prefix {H2O2.prefix} \
                   -LJ_in_file no_lj.txt -charge_in_file no_charge.txt -cv_in_file cv.txt \
                   -cutoff 1 -skin 1 -neighbor_list_refresh_interval 100000 -dihedral_in_file my_dihedral.txt"
    run_command = f"SPONGE -mode NVT -dt 1e-3 -step_limit 1000000 -default_in_file_prefix {H2O2.prefix} \
                   -LJ_in_file no_lj.txt -charge_in_file no_charge.txt -cv_in_file cv.txt \
                   -cutoff 1 -skin 1 -neighbor_list_refresh_interval 100000 -dihedral_in_file my_dihedral.txt \
                   -thermostat middle_langevin -coordinate_in_file restart_coordinate.txt -write_information_interval 100"
    with open("no_charge.txt", "w") as f:
        f.write("4\n0\n0\n0\n0\n")
    with open("no_lj.txt", "w") as f:
        f.write("4 1\n0\n\n0\n\n0\n0\n0\n0\n")
    with open("my_dihedral.txt", "w") as f:
        f.write("2\n2 0 1 3 2 15 0.4\n2 0 1 3 3 5 -0.6\n")
    with open("cv.txt", "w") as f:
        f.write("""torsion
{
CV_type = dihedral
atom = 2 0 1 3
}

meta1d
{
CV = torsion
dCV = 0.001
CV_minimal = -3.142
CV_maximum = 3.142
CV_period = 6.284
welltemp_factor = 50
height = 1
sigma = 0.5
}

print_CV = torsion
""")
    assert os.system(min_command) == 0
    assert os.system(run_command) == 0
    t = MdoutReader("mdout.txt")
    bias = t.meta1d
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
    toread = np.loadtxt("meta1d_potential.txt", skiprows=3)
    toread[:, 1] = -toread[:, 1]
    toread[:, 1] -= np.min(toread[:, 1])
    plt.plot(positions, result, label="simulated results")
    plt.plot(positions, theory, label="potential")
    plt.plot(toread[:, 0], toread[:, 1], label="meta1d potential")
    plt.legend()
    plt.savefig("meta1d.png")
    plt.clf()
