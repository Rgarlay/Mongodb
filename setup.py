## Let's import all the texts/package names here

from setuptools import find_packages, setup
from typing import List


def get_packages() -> List[str]:
    req = []
    try:
        with open('req.txt','r') as files:
            readlines = files.readlines()
            # removing spaces
            for lines in readlines:
                requirments = lines.strip()
            # getting rid of -e .
                if requirments != "-e .":
                    req.append(requirments)
    except Exception as e:
        print(e)
    return req
 
#print(get_packages())

setup(
    name="Project",  # lowercase key
    version="0.0.1",
    author="Ravi Garlay",
    description="MLOps training",
    packages=find_packages(),
    install_requires=get_packages()
)