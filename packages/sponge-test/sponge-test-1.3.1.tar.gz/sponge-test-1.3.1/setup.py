import setuptools
import re, os

f = open("README.rst", "r", encoding="utf-8")
long_description = f.read()
f.close()

with open(os.path.join("sponge_test", "__init__.py")) as f:
    VERSION = re.search(r"__version__\s*=\s*['\"](.+?)['\"]",f.read()).group(1)

setuptools.setup(
    name="sponge-test",
    version=VERSION,
    author="Yijie Xia",  
    author_email="yijiexia@pku.edu.cn", 
    description="A Python package to do the unit test for SPONGE",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    #url="https://gitee.com/gao_hyp_xyj_admin/sponge_test",
    entry_points = {"console_scripts": ["sponge-test = sponge_test.__main__:main"]},
    packages=setuptools.find_packages(),
    package_data = {"":['*.txt', "*.mol2"]},
    install_requires = ["pytest", "Xponge", "MDAnalysis", "numpy", "scipy"],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        'Development Status :: 5 - Production/Stable',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', 
)
