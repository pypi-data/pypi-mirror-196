import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "market-gpt",
    version = "0.3.3",
    author = "Nero Chen",
    author_email = "nerocube.tw@gmail.com",
    description = "Get market sentiment score with the assistance of OpenAI GPT-3.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/NeroCube/market-gpt",
    project_urls = {
        "Bug Tracker": "https://github.com/NeroCube/market-gpt/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "market_gpt"},
    packages = setuptools.find_packages(where="market_gpt"),
    python_requires = ">=3.7.1",
    install_requires=['openai >= 0.26.1'],
    entry_points = {
        'console_scripts': ['market-gpt=market_gpt.__main__:main'],
    }
)