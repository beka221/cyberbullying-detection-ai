from setuptools import setup, find_packages

setup(
    name="cyberbullying-detection-ai",
    version="2.0.0",
    description="Advanced AI-based system for early detection and classification of cyberbullying",
    author="3 Students Team",
    author_email="diploma@cyberbullying-ai.dev",
    url="https://github.com/beka221/cyberbullying-detection-ai",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "scikit-learn>=1.3.0",
        "nltk>=3.8.0",
        "pandas>=2.1.0",
        "numpy>=1.26.0",
        "pydantic>=2.5.0",
        "sqlalchemy>=2.0.0",
        "joblib>=1.3.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ]
)
