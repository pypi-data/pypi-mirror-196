from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="tensorflow-riemopt",
    version="0.1.1",
    description="a library for optimization on Riemannian manifolds",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Oleg Smirnov",
    author_email="oleg.smirnov@gmail.com",
    packages=find_packages(),
    install_requires=["tensorflow==2.6.3"],
    python_requires=">=3.6.0",
    url="https://github.com/master/tensorflow-riemopt",
    zip_safe=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Operating System :: OS Independent",
    ],
    keywords="tensorflow optimization machine learning",
)
