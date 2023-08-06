from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='easystockplot',
    version='0.1.1',
    description='an easy stockplot package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='S Huo',
    url='https://sl-huo.github.io/',
    packages=['easystockplot'],
    install_requires=['yfinance', 'matplotlib', 'seaborn'],
    keywords=['python', 'stock', 'plot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
    )