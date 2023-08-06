from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A library for converting an image to ascii art (simple text and html).'

# Setting up
setup(
    name="ascii_art_library",
    version=VERSION,
    author="AlDim",
    author_email="<aldim.gr@gmail.com>",
    description=DESCRIPTION,
    readme = "README.md",
    packages=find_packages(),
    install_requires=['pil'],
    keywords=['python', 'ascii', 'art', 'generator', 'converter', 'ascii art'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
