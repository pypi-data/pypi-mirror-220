from setuptools import setup, find_packages

VERSION = '0.0.06' 
DESCRIPTION = 'Computer vision package'
LONG_DESCRIPTION = 'This Python package aims to evaluate image in different ways, including emotion (love, joy, surprise, anger, sadness and fear) with computer vision.'


setup(
        name="cvision", 
        version=VERSION,
        author="Dr Anna Sung and Prof Kelvin Leong",
        author_email="<k.leong@chester.ac.uk>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
               
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
