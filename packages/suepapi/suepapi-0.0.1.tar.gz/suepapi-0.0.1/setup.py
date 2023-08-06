from setuptools import setup

setup(
    name='suepapi',
    version='0.0.1',
    include_package_data=True,
    packages=['suepapi'],
    install_requires=[
        'pyquery>=1.4.3',
        'requests>=2.28.1',
        'PySocks>=1.7.1'
    ],
    author='andywang425',
    description='APIs for SUEP websites',
    url='https://github.com/andywang425/suepapi',
    readme = "README.md"
)
