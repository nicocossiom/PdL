from setuptools import setup
setup(
    name='jspdl',
    version='1.0',
    entry_points={
        'console_scripts': [
            'jspdl=jspdl:main'
        ]
    }
)