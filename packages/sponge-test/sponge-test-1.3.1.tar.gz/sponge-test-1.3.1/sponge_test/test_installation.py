"""
check the installation
"""
import os


def test_installation():
    assert os.system("SPONGE -v") == 0
    assert os.system("SPONGE_NOPBC -v") == 0
    assert os.system("SPONGE_TI -v") == 0
    assert os.system("SPONGE_FEP -v") == 0
