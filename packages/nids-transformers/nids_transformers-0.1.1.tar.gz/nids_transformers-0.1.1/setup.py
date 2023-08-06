import setuptools

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='nids_transformers',
    version='0.1.1',
    description="Tag Generation and Text Generation Inference for Network Packets using Transformers",
    keywords="NIDS Transformers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    author="Pahalavan R D",
    author_email='rdpahalavan24@gmail.com',
    packages=['nids_transformers'],
    python_requires='>=3.7.0',
    url='https://github.com/rdpahalavan/BERTSimilarWords',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=requirements
)