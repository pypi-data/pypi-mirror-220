from setuptools import setup 
with open("README.md", "r") as f:
	long_description = f.read()
setup(
name="Queue_Analyzer",
version="0.9.1",
description="python package to retreive youtube comments and translate them",
package_dir={"": "src"},
include_package_data=True,
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/dipson94/Queue-Analyzer",
author="Dipson",
author_email="dipson94.coding@gmail.com",
license="GNU GPL V3",
classifiers=["License :: OSI Approved :: GNU General Public License v3 (GPLv3)","Programming Language :: Python :: 3.10",'Operating System :: POSIX :: Linux','Operating System :: MacOS :: MacOS X',
'Operating System :: Unix'],
install_requires=["matplotlib>=3.5.1","numpy>=1.21.5","pycairo>=1.20.1","pandas>=2.0.1","PyGObject>3.42.0"],
extras_require={
        "dev": ["pytest >= 7.0"]
        },
entry_points={
'console_scripts': ['queueanalyzer=Queue_Analyzer:main',],},
python_requires=">=3.7",    
)
#"PyGObject==3.44.1",
