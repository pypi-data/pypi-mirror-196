import os

from setuptools import setup

consts = {}
with open(os.path.join("elvia", "const.py")) as fp:
    exec(fp.read(), consts)
    
def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="pyElvia",
    long_description_content_type='text/markdown',
    long_description=readme(),
    packages=["elvia"],
    install_requires=[
        "urllib3>=1.26.12",
        "aiohttp>=3.8.1"
    ],
    version=consts["__version__"],
    description="""A python3 library to read meter from Elvia""",
    python_requires=">=3.9.0",
    author="Brage Skjønborg",
    author_email="bskjon@outlook.com",
    url="https://github.com/bskjon/pyElvia",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Home Automation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
