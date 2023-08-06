from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'Python package to help with HTML development.'

with open("README.md", 'r') as f:
    long_description = f.read()
    
# Setting up
setup(
        name="alienHTML", 
        version=VERSION,
        author="TomTheCodingGuy",
        author_email="<tomb80940@gmail.com>",
        description=DESCRIPTION,
        long_description_content_type="text/markdown",
        long_description=long_description,
        url="https://github.com/TomTheCodingGuy/alienHTML",
        packages=find_packages(),
        install_requires=["pillow"],
        python_requires='>=3.7',
        keywords=['python', 'html', 'alien', 'alienHTML'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)