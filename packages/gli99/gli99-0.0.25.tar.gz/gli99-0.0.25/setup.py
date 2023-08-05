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
    version='0.0.25',
    description=description,
    package_dir={'':'src'},
    packages=setuptools.find_packages(where="src"),
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
    install_requires=[
        'selenium',
        'requests',
    ],
    url=f"https://github.com/TomTkacz/{repo_name}",
    author="Tom Tkacz",
    author_email="thomasatkacz@gmail.com",
)