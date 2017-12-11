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
        "Natural Language :: Russian",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    keywords=(
        "vladya rus russian phonetic"
    ),
    description="Phonetic analysis of the words of the Russian language.",
    long_description=(
        "Фонетический разбор слов русского языка."
    )
)
