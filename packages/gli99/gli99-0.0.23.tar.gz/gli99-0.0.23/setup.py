import setuptools

repo_name = "gli99"
pip_name = "gli99"
description = ""
modules = [
    "gli99",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=pip_name,
    version='0.0.23',
    description=description,
    packages=setuptools.find_packages(),
    package_dir={'':'src'},
    package_data={'':['*.json','*.py'],},
    include_package_data=True,
    python_requires=">3.10.0",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={
        "dev": [
            "pytest>=3.7",
        ]
    },
    install_requires=[
        'selenium',
        'requests',
    ],
    url=f"https://github.com/TomTkacz/{repo_name}",
    author="Tom Tkacz",
    author_email="thomasatkacz@gmail.com",
)