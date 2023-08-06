from setuptools import setup, find_packages

VERSION="v1.2.1"
DESCRIPTION = 'A fun little python package including tools such as math, encryption, and ANSI color codes.'
LONG_DESCRIPTION = 'NOTE: THIS VERSION (v1.2.1) IS THE FIRST STABLE VERSION. OTHER VERSIONS HAVE IMPORTING ISSUES AND ERRORS IN CODE. DO NOT USE THEM.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="phoenixtools", 
        version=VERSION,
        author="Jack B.",
        author_email="<BurrJ22@outlook.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # need to be installed along with your package. Eg: 'caer'
        
        keywords=['python','encryption','PyPi','math','Steam Keygen'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)