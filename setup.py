# setup.py
from setuptools import setup, find_packages

setup(
    name="horse-game-api",
    version="0.1.0",
    packages=find_packages(exclude=["tests*",]),
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn>=0.22.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "pydantic>=2.0.0",
        "passlib[bcrypt]>=1.7.0",
        "python-jose[cryptography]>=3.0.0",
        "httpx>=0.24.0",      # для тестов
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-anyio>=3.0.0",
            "pre-commit",
        ]
    },
    python_requires=">=3.10",
)
