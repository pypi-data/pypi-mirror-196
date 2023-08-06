from setuptools import find_packages, setup
from os import path

root_dir = path.abspath(path.dirname(__file__))


def read(*parts):
    with open(path.join(root_dir, *parts), encoding="utf-8") as f:
        return f.read()


setup(
    name="contrast-agent-lib",
    version="0.5.3",
    description="Python interface to the contrast agent lib",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://www.contrastsecurity.com",
    project_urls={
        "Support": "https://support.contrastsecurity.com",
    },
    # Author details
    author="Contrast Security, Inc.",
    author_email="python@contrastsecurity.com",
    # Choose your license
    license="CONTRAST SECURITY (see LICENSE.txt)",
    license_files=("LICENSE.txt",),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    # See MANIFEST.in for excluded packages
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"contrast_agent_lib": ["libs/libcontrast_c*"]},
    python_requires=">=3.7",
)
