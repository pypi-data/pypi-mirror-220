import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    # long_description = fh.read()
    long_description=''

setuptools.setup(
    name="AndroidN",
    version="0.0.4",
    author="1a",
    author_email="grayrail1x3@gmail.com",
    description="Android",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grayrail000/AndroidQ.git",
    packages=setuptools.find_packages(),
    package_data={
        "": ["*.dll"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
