from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Basic hello'
# Setting up
setup(
    name="dptest",
    version=VERSION,
    author="My Name",
    author_email="<pth.a15.33.tran.thien@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'test'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ]
)