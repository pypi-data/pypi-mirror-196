from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()


long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='suepapi',
    version='0.0.2',
    include_package_data=True,
    packages=['suepapi'],
    install_requires=[
        'pyquery>=1.4.3',
        'requests>=2.28.1',
        'PySocks>=1.7.1'
    ],
    author='andywang425',
    description='APIs for SUEP websites',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/andywang425/suepapi',
    python_requires=">=3.7",
    project_urls={
        "Bug Reports": "https://github.com/andywang425/suepapi/issues",
        "Source": "https://github.com/andywang425/suepapi"
    }
)
