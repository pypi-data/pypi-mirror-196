from setuptools import setup, find_packages

VERSION = '1.1' 
DESCRIPTION = 'scan 3d package by xxp'
LONG_DESCRIPTION = 'scan 3d python package designed by xinping xu'

#setting
setup(
        name = "scan_3d_by_xxp", 
        version = VERSION,
        author = "Xinping Xu",
        author_email = "<xuxinping92@gmail.com>",
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        packages = find_packages(),
        install_requires = ['numpy', 'pandas'], # add any additional packages that we need to install, i.e., 'caer'
                                   
        keywords = ['python', 'first package'],
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            ]
        )
