from setuptools import setup

setup(
    name='gmap',
    version='1.2',
    py_modules=['gmap'],
    entry_points='''
        [console_scripts]
        gmap=gmap:cli
    ''',
)

