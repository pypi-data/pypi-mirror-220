from setuptools import setup

readme = open("./README.md", "r")

setup(
    name="paucode",
    packages=["paucode"],
    version="0.1",
    description="funciones de ayuda en trabajo como economista",
    long_description=readme.read(),
    long_description_content_type="text/markdown",
    author="Javier Choque Paucar",
    author_email="choquepaucarj.social@gmail.com",
    download_url="https://github.com/paucode1/paucode",
    keywords=["example"],
    classifiers=[],
    license="MIT",
    include_package_data=True
)