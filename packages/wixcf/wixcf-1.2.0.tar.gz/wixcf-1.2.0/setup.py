from setuptools import setup

setup(
    name="wixcf",
    version="1.2.0",
    author="Aras Tokdemir",
    author_email="aras.tokdemir@outlook.com",
    description="Wix Package",
    packages=["Wix"],
    install_requires=[
        "wikipedia",
        "numpy",
        "pandas",
        "cryptocompare",
        "keras",
        "tensorflow",
        "faker",
    ],
    entry_points={
        "console_scripts": [
            "wix = Wix.main:main"
        ]
    },
)
