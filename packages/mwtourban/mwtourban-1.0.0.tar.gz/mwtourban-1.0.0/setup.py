from setuptools import setup, find_packages
import pathlib
setup(
    name='mwtourban',
    version='1.0.0',
    license='MIT License',
    platforms='any',
    install_requires=["time", "pymysql",'numpy','pandas']
)