import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="who_added_this_tag",
    version="0.0.1",
    author="Mateusz Konieczny",
    author_email="matkoniecz@tutanota.com",
    description="A tool to research who added given OSM tags currently in use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/matkoniecz/who-added-this-tag",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    # for dependencies syntax see https://python-packaging.readthedocs.io/en/latest/dependencies.html
) 
