import setuptools

setuptools.setup(
    name="sfdc-dummy",
    version="1.0.10",
    author="Nick Le Mouton",
    author_email="nlemouton@salesforce.com",
    description="just a test package",
    packages=setuptools.find_packages(exclude=["*tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6'
)
