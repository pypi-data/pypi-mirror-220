import sys
from pathlib import Path

from setuptools import setup

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))  # for setuptools.build_meta


def get_long_description() -> str:
    return (
        (CURRENT_DIR / "README.md").read_text(encoding="utf8")
        + "\n\n"
        + (CURRENT_DIR / "CHANGELOG.md").read_text(encoding="utf8")
    )


setup(
    name="pyaugmecon",
    version="1.0.1",
    author="Wouter Bles",
    author_email="whbles@gmail.com",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="python, pyomo, optimization, multi-objective-optimization, augmecon",
    url="https://github.com/wouterbles/pyaugmecon",
    project_urls={"Changelog": "https://github.com/wouterbles/pyaugmecon/blob/main/CHANGELOG.md"},
    license="MIT",
    packages=["pyaugmecon"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Education",
    ],
    test_suite="tests",
    python_requires=">=3.8",
    install_requires=[
        "pyomo>=6.4,<6.5",
        "numpy>=1.2,<1.25",
        "pandas>=1.2,<1.6",
        "cloudpickle>=2.0,<2.3",
        "pymoo>=0.6,<0.7",
        "openpyxl>=3.0,<3.1",
    ],
)
