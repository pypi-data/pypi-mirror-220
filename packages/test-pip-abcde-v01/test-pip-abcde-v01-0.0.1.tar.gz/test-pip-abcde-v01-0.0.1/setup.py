import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test-pip-abcde-v01",
    version="0.0.1",
    author="Camilo Akimushkin Valencia",
    author_email="camilo.akimushkin@gmail.com",
    description="A small example package to test pip v01",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/camiloakv/test-pip-abcde-v01",
    packages=["test_pip_abcde_v01"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)