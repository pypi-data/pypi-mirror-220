from setuptools import setup

setup(
    name='mcu-geo-utils',
    version='0.1',
    author='Martin Conur',
    author_email='martincontrerasur@gmail.com',
    packages=['mcu_geo_utils'],
    scripts=[],
   # url='http://pypi.python.org/pypi/apiweather/',
    license='MIT',
    description='variaty of geo-related tools',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas >= 1.5.1",
        "geopandas == 0.12.1",
        "shapely == 2.0.1",
        "osmnx == 1.5.1"
    ],
)