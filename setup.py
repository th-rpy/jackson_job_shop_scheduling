import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JackPy",
    version="0.0.1",
    author="Saraei Thamer",
    author_email="thamer.saraei@polymtl.ca",
    description="Python package to solve the job shop scheduling problem with Gantt chart as output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/th-rpy/jackson_job_shop_scheduling",
    project_urls={
        "Bug Tracker": "https://github.com/th-rpy/jackson_job_shop_scheduling/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
