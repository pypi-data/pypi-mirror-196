""" setuptools """
import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name = 'mlopsdna',
    version = '0.0.9',
    author = 'ramenz',
    author_email = 'ramenz@juno.com',
    description = 'experimental ml libraries',
    url = '',
    packages = setuptools.find_packages(),
    package_data = {
      '': ['static/*'],
      '': ['data/*.csv']
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
