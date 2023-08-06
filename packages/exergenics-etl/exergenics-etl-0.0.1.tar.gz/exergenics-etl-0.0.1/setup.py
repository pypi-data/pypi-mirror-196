from setuptools import find_packages, setup

with open("app/Readme.md", "r") as f:
    long_description = f.read()

setup(
    name="exergenics-etl",
    version="0.0.1",
    description="Exergenics shared Data ETL functions",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Nobel Wong",
    author_email="nobel.wong@exergenics.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ],
    install_requires=["exergenics >= 2.0.0"],
    extras_require={
        "dev": ["pytest >= 7.0", "twine >= 4.0.2", "bump == 1.3.2"],
    },
    python_requires=">=3.8.10"
)
