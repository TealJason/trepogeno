from setuptools import setup, find_packages

setup(
    name="genotreponema",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "genotreponema=nextstrain.nextstrain.genotreponema.cli:main",
        ],
    },
    install_requires=[
        # add any dependencies you need here
    ],
    author="Jason Beard",
    description="CLI for summarizing Treponema lineage calls",
    zip_safe=False,
)
