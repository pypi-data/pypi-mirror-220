import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test-pip-abcde-camilo",
    version="0.0.1",
    author="Camilo Akimushkin Valencia",
    author_email="camilo.akimushkin@gmail.com",
    description="A small example package to test pip",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/camiloakv/test-pip-abcde",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)