"""
Check the thermostat
"""
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from Xponge.analysis import wham
from sponge_test import H2O2

def setup_module():
    if os.path.exists("umbrella"):
        shutil.rmtree("umbrella")
    os.mkdir("umbrella")
    os.chdir('umbrella')

def teardown_module():
    os.chdir('..')

def test_umbrella():
    min_command = f"SPONGE -mode minimization -step_limit 10000 -default_in_file_prefix {H2O2.prefix} \
                   -LJ_in_file no_lj.txt -charge_in_file no_charge.txt -cv_in_file cv.txt \
                   -cutoff 1 -skin 1 -neighbor_list_refresh_interval 100000 -dihedral_in_file my_dihedral.txt"
    run_command = f"SPONGE -mode NVT -dt 1e-3 -step_limit 20000 -default_in_file_prefix {H2O2.prefix} \
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

restrain
{
CV = torsion
weight = 200
reference = res_cv_ref
period = pi2
}

print_CV = torsion
""")


    for i, ref in enumerate(np.linspace(-np.pi,np.pi,50)):
        assert os.system(min_command + f" -res_cv_ref {ref} -pi2 {2 * np.pi}") == 0
        assert os.system(run_command + f" -res_cv_ref {ref} -pi2 {2 * np.pi}") == 0
        shutil.copy("mdout.txt", f"{i}.mdout")

    w = wham.WHAM(np.linspace(-np.pi, np.pi, 51), 300, 200, np.linspace(-np.pi, np.pi, 50), 2 * np.pi)
    w.get_data_from_mdout("*.mdout", "torsion")
    x, y, f = w.main()
    plt.plot(f)
    plt.savefig("free_energy_of_simulations.png")
    plt.clf()
    plt.plot(x, y, label="umbrella sampling")
    y2 = 15 * np.cos(2 * x - 0.4) + 5 * np.cos(3 * x + 0.6)
    y2 -= min(y2)
    plt.plot(x, y2, label="potential")
    plt.legend()
    plt.savefig("sampling.png")
    plt.clf()
