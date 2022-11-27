from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
  "ipython>=6", 
  "nbformat>=4", 
  "nbconvert>=5", 
  "requests>=2"
]

setup(
    name="notebookc",
    version="0.0.1",
    author="Nathaniel Reeves",
    author_email="nathaniel.jacob.reeves@gmail.com",
    description="A api to run a heads-up chrome extension",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Milestone3SE3400/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
