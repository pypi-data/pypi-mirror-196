import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meshflow",
    version="0.0.1",
    author="Shenggan Cheng",
    author_email="shenggan.c@u.nus.edu",
    description="Efficient Automatic Training System for Super-Large Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shenggan/meshflow",
    packages=setuptools.find_packages(),
)