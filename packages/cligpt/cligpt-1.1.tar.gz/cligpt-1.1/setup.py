import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cligpt",
    version="1.1",
    author="skvn",
    author_email="xxx@gmail.com",
    description="A handy CLI interface for ChatGPT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.example.com/~cschultz/bvote/",
    project_urls={
        "Bug Tracker": "http://bitbucket.org/tarek/distribute/issues/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
                                                                               # package_dir={"": "cligpt"},
                                                                               # packages=setuptools.find_packages(where="cligpt"),
    python_requires=">=3.6",
    install_requires=['openai'],
    package_data={"": ["cligpt/config.json"]},
    include_package_data=True,
    entry_points={
        "console_scripts": ["cligpt = cligpt.cli:main"],
    },
)
