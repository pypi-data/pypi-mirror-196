import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="corpusshow",
    version="0.1.7",
    author="parkminwoo",
    author_email="parkminwoo1991@gmail.com",
    description="Corpus-Show makes it easier and faster to visualize corpus through sentence embedding of corpus.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DSDanielPark/corpus-show",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
    "transformers", "tokenizer",
        "sentence-transformers",
        "quickshow",
    ])