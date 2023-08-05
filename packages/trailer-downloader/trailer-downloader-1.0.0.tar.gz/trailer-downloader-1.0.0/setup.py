from setuptools import setup

setup(
    name="trailer-downloader",
    version="1.0.0",
    description="Downloader of trailers for films/series",
    url="https://github.com/Steelataure/Trailer-downloader",
    author="Alexandre Buisset",
    author_email="alexandre0312@orange.fr",
    license="MIT",
    keywords=["trailer", "downloader"],
    py_modules=["main"],
    install_requires=[
        "pytube"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
