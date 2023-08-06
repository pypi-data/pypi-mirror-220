import setuptools

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='nids_datasets',
    version='0.1.3',
    description="Download and utilize specially curated and extracted datasets from the original UNSW-NB15 and CIC-IDS2017 datasets",
    keywords="Dataset NIDS UNSW-NB15 CIC-IDS2017",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    author="Pahalavan R D",
    author_email='rdpahalavan24@gmail.com',
    packages=['nids_datasets'],
    python_requires='>=3.7.0',
    url='https://github.com/rdpahalavan/nids-datasets',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements
)