from setuptools import setup

setup(
    name='easystockplot',
    version='0.1',
    description='an easy stockplot package',
    author='S Huo',
    url='https://sl-huo.github.io/',
    packages=['easystockplot'],
    install_requires=['yfinance', 'matplotlib', 'seaborn'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
    )