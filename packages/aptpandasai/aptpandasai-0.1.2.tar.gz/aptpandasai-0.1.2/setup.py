from setuptools import setup

setup(
    name = 'aptpandasai',
    version = '0.1.2',
    packages = ['pai'],
    entry_points = {
        'console_scripts': [
            'pai = pai.__main__:main'
        ]
    }
)