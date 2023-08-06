from setuptools import setup

setup(
    name='mcu-geo-utils',
    version='0.4',
    author='Martin Conur',
    author_email='martincontrerasur@gmail.com',
    packages=['mcu_geo_utils'],
    scripts=[],
    url='https://pypi.org/project/mcu-geo-utils/',
    license='MIT',
    description='variaty of geo-related tools',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas >= 1.0",
        "geopandas == 0.10.1",
        "shapely == 2.0.1",
        "osmnx == 1.5.1"
    ],
)
