import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mentioner",  # Replace with your own username
    version="0.0.1",
    author="Błażej Rybarkiewicz",
    author_email="b.rybarkiewicz@gmail.com",
    description="Mentioner module for Piłkomentarz project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abryb/bbgh-mentioner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)