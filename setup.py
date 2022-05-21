from setuptools import setup


setup(
    name="dl-cli",
    version="0.0.1",
    install_requires=["deepl"],
    entry_points={
        "console_scripts": [
            "dl-cli = dlcli:main",
        ],
    }
)
