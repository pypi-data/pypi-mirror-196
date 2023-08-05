import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'mlopsdna',
    version = '0.0.6',
    author = 'ramenz',
    author_email = 'ramenz@juno.com',
    description = 'experimental libraries',
    url = '',
    packages = setuptools.find_packages(),
    classifiers = [
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
)
