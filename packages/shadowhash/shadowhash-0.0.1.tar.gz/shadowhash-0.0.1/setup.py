import setuptools

name = "shadowhash"

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

version_file = "{}/version.py".format(name)
with open(version_file) as fi:
    vs = {}
    exec(fi.read(), vs)
    __version__ = vs["__version__"]

setuptools.setup(
    name=name,
    version=__version__,
    author="Eloy Perez",
    author_email="zer1t0ps@protonmail.com",
    description="Generate /etc/shadow crypt hashes",
    url="https://gitlab.com/zer1t0/shadowhash",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "shadowhash = shadowhash.__main__:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
