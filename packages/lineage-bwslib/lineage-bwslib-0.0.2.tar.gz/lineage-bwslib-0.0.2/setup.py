import setuptools

setuptools.setup(
    name="lineage-bwslib",
    version="0.0.2",
    description="BWS auth lib package",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires = ["jwt", "requests", "retrying", "urllib3"],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
