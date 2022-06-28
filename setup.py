import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nswsigns",
    author="Darcy Raimond",
    author_email="darcy.raimond@gmail.com",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=["opencv"]
)