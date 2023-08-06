from setuptools import setup

try:
    version = open("version", "r").read().strip()
except FileNotFoundError:
    version = 0

setup(
    name="challenge.report-generation",
    description="Tool for computing the PnL.",
    author="Begona Gonzalez",
    version=version,
    license="",
    install_requires=["dateparser",
                      "sqlalchemy",
                      "psycopg2"],
    scripts=["bin/report_generation.py"],
)
