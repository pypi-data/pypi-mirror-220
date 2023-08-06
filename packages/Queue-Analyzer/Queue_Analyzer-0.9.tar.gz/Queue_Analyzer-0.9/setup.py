from setuptools import setup
    
with open("README.md", "r") as f:
	long_description = f.read()

setup(
name="Queue_Analyzer",
version="0.9",
description="python package to retreive youtube comments and translate them",
package_dir={"": "src"},
include_package_data=True,
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/dipson94/Queue-Analyzer",
author="Dipson",
author_email="dipson94.coding@gmail.com",
license="GNU GPL V3",
classifiers=["License :: OSI Approved :: GNU General Public License v3 (GPLv3)","Programming Language :: Python :: 3.10","Operating System :: OS Independent"],
install_requires=["matplotlib==3.7.2","numpy==1.25.1","pycairo==1.24.0","PyGObject==3.44.1","pandas==2.0.1",],
extras_require={
        "dev": ["pytest >= 7.0"]
        },
entry_points={
'console_scripts': ['queueanalyzer=Queue_Analyzer:main',],},
python_requires=">=3.10",    
)
