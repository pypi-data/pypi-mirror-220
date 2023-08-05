import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "fuzzy_magic",
    version = "0.1.2",
    author = "Pedro López",
    author_email = "p.lopez@exus.ai",
    url = "https://github.com/EXUS-AI-Labs/ailabs-fuzzylogic",
    description = "A Fuzzy Logic library to create Mamdani Fuzzy Systems the easiest way possible",
    long_description = long_description,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
    packages = ['fuzzy_magic'],
    python_requires = ">=3.6"
)