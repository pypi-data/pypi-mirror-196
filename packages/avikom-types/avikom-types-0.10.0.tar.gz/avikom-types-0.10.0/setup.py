from setuptools import setup, find_packages
import os
import codecs
from os.path import join

project_root = os.path.dirname(os.path.abspath(__file__))
packages = find_packages(exclude="test")

version = {}
REQUIRED_EXTRAS = {}
with open(join(project_root, "avikom_types/version.py")) as read_file:
    exec(read_file.read(), version)

with open(join(project_root, "requirements.txt")) as read_file:
    REQUIRED = []
    for req in read_file.read().splitlines():
        if req.startswith("git+"):
            package = req.split("egg=")[1]
            req = f"{package} @ {req}"
        elif req.startswith("#"):
            continue
        REQUIRED.append(req)

# print("REQ:", REQUIRED)
with codecs.open(join(project_root, "README.md"), "r", "utf-8") as f:
    long_description = "".join(f.readlines())

setup(
    name="avikom-types",
    version=version["__version__"],
    description="Avikom Protocol Buffer Types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=packages,
    package_data={package: ["py.typed", "*.pyi"] for package in packages},
    zip_safe=False,
    install_requires=REQUIRED,
    author="Alexander Neumann",
    author_email="alneuman@techfak.uni-bielefeld.de",
    keywords=["avikom, protocol buffers"],
    url="https://gitlab.ub.uni-bielefeld.de/avikom/converter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
    ],
)
