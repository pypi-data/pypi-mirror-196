import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ysc2-sdk",
    version="0.0.4",
    author="Yang",
    author_email="yangruoyu000@live.com",
    description="A simple API for Yeaosound Chain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.yeaosound.com/yeaosound/ysc/public/ysc-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "OpenSSL":"pyOpenSSL"
    },
    install_requires=[
        "requests",
        "rsa"
    ]
)
