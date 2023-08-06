import setuptools

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecmind_blue_client_asyncio",
    version="0.0.2",
    author="Ulrich Wohlfeil, Roland Koller",
    author_email="info@ecmind.ch",
    description="A asyncio client wrapper for blue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.ecmind.ch/open/ecmind_blue_client_asyncio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=["asyncio-connection-pool"],
    extras_require={
    },
)
