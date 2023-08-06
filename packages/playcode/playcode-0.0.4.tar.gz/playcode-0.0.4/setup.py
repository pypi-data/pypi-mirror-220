import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="playcode", # Replace with your own PyPI username(id)
    version="0.0.4",
    author="Seungjun Min",
    author_email="sjmin213@gmail.com",
    description="Creating password",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sjmin/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)