from setuptools import find_packages, setup
import pathlib

setup(
    name="cify",
    version="0.0.2",
    author="AEPG",
    packages=find_packages(),
    description="A framework that provides the ability to easily and reliably implement nature-inspired "
                "optimization meta-heuristics.",
    license="MIT",
    url="https://github.com/KyleErwin/cify",
    keywords="cify, computational intelligence, optimization, nature-inspired",
    install_requires=pathlib.Path("requirements.txt").read_text().replace("==", ">="),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
