"""
check the minimization system
"""
import os
import shutil
from sponge_test import bad_water, H2O2, bad_dipeptide, ala12

def setup_module():
    if os.path.exists("min"):
        shutil.rmtree("min")
    os.mkdir("min")
    os.chdir('min')

def teardown_module():
    os.chdir('..')

def test_minimization():
    assert os.system(f"SPONGE -mode minimization -step_limit 5000 -default_in_file_prefix {bad_water.prefix} -constrain_mode SHAKE") == 0
    assert os.system(f"SPONGE -mode NVE -dt 2e-3 -step_limit 2000 -default_in_file_prefix {bad_water.prefix} -constrain_mode SHAKE -coordinate_in_file restart_coordinate.txt") == 0
    assert os.system(f"SPONGE -mode minimization -step_limit 5000 -default_in_file_prefix {H2O2.prefix} -constrain_mode SHAKE") == 0
    assert os.system(f"SPONGE -mode NVE -dt 2e-3 -step_limit 2000 -default_in_file_prefix {H2O2.prefix} -constrain_mode SHAKE -coordinate_in_file restart_coordinate.txt") == 0
    assert os.system(f"SPONGE -mode minimization -step_limit 5000 -default_in_file_prefix {bad_dipeptide.prefix} -constrain_mode SHAKE") == 0
    assert os.system(f"SPONGE -mode NVE -dt 2e-3 -step_limit 2000 -default_in_file_prefix {bad_dipeptide.prefix} -constrain_mode SHAKE -coordinate_in_file restart_coordinate.txt") == 0
    assert os.system(f"SPONGE_NOPBC -mode minimization -step_limit 5000 -default_in_file_prefix {ala12.prefix} -constrain_mode SHAKE") == 0
    assert os.system(f"SPONGE_NOPBC -mode NVE -dt 2e-3 -step_limit 2000 -default_in_file_prefix {ala12.prefix} -constrain_mode SHAKE -coordinate_in_file restart_coordinate.txt") == 0
