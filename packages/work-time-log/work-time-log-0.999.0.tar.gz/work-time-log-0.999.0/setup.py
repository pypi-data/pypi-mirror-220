from setuptools import setup
import os

VERSION = "0.999.0"


setup(
    name="work-time-log",
    description="work-time-log is now work",
    long_description="""# work-time-log is now work

This package has been renamed. Use `pipx install work` instead.

New package: https://pypi.org/project/work/""",
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["work"],
    classifiers=["Development Status :: 7 - Inactive"],
)
