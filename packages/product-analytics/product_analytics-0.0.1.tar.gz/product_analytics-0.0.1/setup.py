from setuptools import setup, find_packages

setup(
    name="product_analytics",
    version="0.0.1",
    description="Segment analytics library",
    author="Peak",
    author_email="will.kreitz@peak.ai",
    url="https://github.com/peak-platform/product-analytics-py",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7, <4",
    install_requires=[
        "analytics-python>=1.2.9",
    ],
    extras_require={
        "dev": [
            "black==23.7.0",
            "pytest==7.4.0",
            "pre-commit==3.3.3",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)
