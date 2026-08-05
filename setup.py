from setuptools import setup, find_packages

setup(
    name="unlimited-ai-agent",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
    ],
)
