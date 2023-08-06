from setuptools import setup

setup(
    name="cbquant",
    include_package_data=True,
    long_description_content_type="text/markdown",
    install_requires=[
        "libimagequant",
        "libimagequant-integrations",
        "Pillow",
        "tqdm"
    ],
    extra_require={
        "dev": [
            "pytest"
        ]
    }
)