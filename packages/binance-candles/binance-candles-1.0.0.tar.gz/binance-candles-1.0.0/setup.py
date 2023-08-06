"""Setup for the binance_candles package."""

import io
import setuptools

with io.open("README.md") as fd:
    setuptools.setup(
        author="Alexander Marinov",
        author_email="amarinov@gmail.com",
        name="binance-candles",
        license="MIT",
        description="Provides python generator for crypto currency candles via Binance Socket API",
        long_description=fd.read(),
        long_description_content_type="text/markdown",
        version="v1.0.0",
        url="https://github.com/alekmarinov/binance-candles",
        packages=setuptools.find_packages(),
        python_requires=">=3.6",
        install_requires=["python-binance==1.0.17"],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Intended Audience :: Developers",
            "Intended Audience :: Financial and Insurance Industry",
        ],
    )
