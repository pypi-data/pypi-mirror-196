from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Streaming video data via networks'

with open("Readme.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="Pequena",
    version=VERSION,
    author="borecjeborec1",
    author_email="<atzuki@protonmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pywebview'],
    keywords=['python', 'video', 'stream',
              'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
