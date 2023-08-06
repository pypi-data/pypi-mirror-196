from setuptools import setup, find_packages
import subprocess

with open("README_pypi.md", "r") as readme_file:
    readme = readme_file.read()
    
# with open('requirements_dev.txt', mode='r') as f:
#     requirements = f.read().splitlines()

requirements = [
    "dostoevsky==0.6.0",
    "morpholog==1.6",
    "numpy==1.19.5",
    "pandas==1.3.5",
    "pingouin==0.3.11",
    "pymorphy2==0.9.1",
    "pymystem3==0.2.0",
    "seaborn==0.11.2",
    "simple-elmo==0.8.0",
    "snowballstemmer==2.1.0",
    "spacy==3.0.6",
   "stanza==1.2",
    "tensorflow==2.5.0",
    "termcolor==1.1.0",
    "wordfreq==2.5.0"
    ]

setup(
    name="analytics_lib",
    version="0.0.2",
    author="Pokhachevskiy Vsevolod",
    author_email="pokhachevskiy@gmail.com",
    description="A package for psychotyping by text",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/lyoshamipt/bortnik_psychometry",
    packages=find_packages(),
    install_requires=requirements,
    # classifiers=[
    #     "Programming Language :: Python :: 3.8.9",
    #     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    # ],
)