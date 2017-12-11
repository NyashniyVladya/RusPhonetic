from setuptools import setup, find_packages
import RusPhonetic

setup(
    name="RusPhonetic",
    version=RusPhonetic.__version__,
    author=RusPhonetic.__author__,
    url="https://github.com/NyashniyVladya/RusPhonetic",
    packages=find_packages(),
    python_requires=">=3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GENERAL PUBLIC LICENSE"
    ],
    keywords=(
        "vladya rus russian phonetic"
    ),
    description="Phonetic analysis of the words of the Russian language.",
    long_description=(
        "Фонетический разбор слов русского языка."
    )
)
