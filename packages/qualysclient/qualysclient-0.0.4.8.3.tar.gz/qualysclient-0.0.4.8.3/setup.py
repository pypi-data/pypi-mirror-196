from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open("qualysclient/version.py").read())

setup(
    name="qualysclient",
    version=__version__,
    author="Wood Techie",
    author_email="woodtechie1428@gmail.com",
    description="Python SDK for interacting with the Qualys API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woodtechie1428/qualysclient",
    project_urls={
        "Bug Tracker": "https://github.com/woodtechie1428/qualysclient/issues",
        "Documentation": "https://qualysclient.readthedocs.io/en/latest/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    py_modules=["qualysclient"],
    install_requires=["requests", "lxml"],
)
