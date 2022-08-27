from setuptools import setup

setup(
    name="robot_scraping",
    version="0.1.0",
    description="Python Distribution Utilities",
    author="Walter Leskovar",
    author_email="wleskovar@gmail.com",
    packages=["robot_scraping"],
    install_requires=[
        "sqlalchemy>=1.4.39"
        "requests>=2.28.1"
        "openpyxl>=3.0.10"
        "pandas>=1.4.3"
        "psycopg2>=2.9.3"
        "python-decouple>=3.6"
        "python-dotenv>=0.20.0"
        "webdrivermanager>=0.10.0"
    ],
)
