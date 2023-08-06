import setuptools
from pathlib import Path



setuptools.setup(
    name="bathazarepdf",
    version="1.0",
    author="Bathazare PAIGE",
    author_email="me@bathazarepaige.com",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests","data"]),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)