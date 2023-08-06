import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="fuxien",
  version="0.0.2",
  author="Lixver",
  author_email="Lixver@outlook.com",
  description="A simple cryptographic library",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Lixver",
  packages=["fuxien"],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)