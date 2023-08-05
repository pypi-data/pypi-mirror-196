from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Python package to help with HTML development.'
LONG_DESCRIPTION = 'Python package to help build and edit html files.'

# Setting up
setup(
        name="alienHTML", 
        version=VERSION,
        author="TomTheCodingGuy",
        author_email="<tomb80940@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["pillow"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'html', 'alien'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)