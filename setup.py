import sys,os
from setuptools import setup
from distutils.cmd import Command
from distutils.errors import DistutilsExecError

setup(
    packages=[],
    name='start-wifi.py',
    version='1.0.0',
    author='Anthony Guevara',
    author_email='amboxer21@gmail.com',
    license='GPL-3.0',
    install_requires=[
        'pyroute2',
    ],
    url='https://github.com/amboxer21/StartWifiPy',
    description="StartWifiPy manages non-encrypted network connections for my Gentoo box.",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
    cmdclass={ },
)
