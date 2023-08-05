import setuptools

long_description = ""

req = [
       ]

setuptools.setup(
    name="tencirchem",
    version="0.0.1",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    install_requires=req,
)


# How to publish the library to pypi
# python setup.py sdist
# twine upload -s dist/*
