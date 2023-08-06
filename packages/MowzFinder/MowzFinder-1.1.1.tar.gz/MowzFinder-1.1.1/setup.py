from setuptools import setup, find_packages

VERSION = '1.1.1'
DESCRIPTION = 'You Can Find WebPages Of A Website'

# Setting up
setup(
    name="MowzFinder",
    version=VERSION,
    author="DrMowz",
    author_email="<drmowz8585@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests','colorama'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)