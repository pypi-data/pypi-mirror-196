from setuptools import setuptools
setuptools.setup(
    name='DiffehellmanAlphaCalculator',
    version='0.2',
    author="RAVINDRA HV",
    author_email="ravindrahvasudeva@gmail.com",
    long_description="In Diffehellman key exchange technique we calculate Alpha value .Which should be primitive root of the given prime number,hence this package solve the trouble of finding the Alpha .",
    short_description="DiffehellmanAlphaCalculator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
