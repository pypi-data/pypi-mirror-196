"""
Check the thermostat
"""
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from Xponge.analysis import MdoutReader
from sponge_test import water

def setup_module():
    if os.path.exists("thermostat"):
        shutil.rmtree("thermostat")
    os.mkdir("thermostat")
    os.chdir('thermostat')

def teardown_module():
    os.chdir('..')

def test_thermostat():
    basic_command = f"SPONGE -mode NVT -dt 2e-3 -step_limit 100000 \
 -write_information_interval 100 -default_in_file_prefix {water.prefix} -constrain_mode SHAKE "
    assert os.system(basic_command + "-thermostat middle_langevin") == 0
    shutil.copy("mdout.txt", "middle_langevin.mdout")
    assert os.system(basic_command + "-thermostat andersen_thermostat") == 0
    shutil.copy("mdout.txt", "andersen_thermostat.mdout")
    assert os.system(basic_command + "-thermostat berendsen_thermostat") == 0
    shutil.copy("mdout.txt", "berendsen_thermostat.mdout")
    assert os.system(basic_command + "-thermostat berendsen_thermostat -berendsen_thermostat_stochastic_term 1") == 0
    shutil.copy("mdout.txt", "berendsen_thermostat_fix.mdout")
    assert os.system(basic_command + "-thermostat nose_hoover_chain") == 0
    shutil.copy("mdout.txt", "nose_hoover_chain.mdout")
    for i in ["middle_langevin", "andersen_thermostat", "berendsen_thermostat", "berendsen_thermostat_fix", "nose_hoover_chain"]:
        temperatures = MdoutReader(f"{i}.mdout").temperature[100:]
        x = np.linspace(290, 310, 300)
        y = gaussian_kde(temperatures)(x)
        plt.plot(x, y, label=i)
        assert abs(np.mean(temperatures) - 300) < 2, i
    plt.legend()
    plt.savefig("thermostat.png")
    plt.clf()
