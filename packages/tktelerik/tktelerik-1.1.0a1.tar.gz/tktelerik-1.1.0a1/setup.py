from setuptools import find_packages, setup

setup(
    name="tktelerik",
    version="1.1.0a1",
    author="XiangQinxi",
    author_email="XiangQinxi@outlook.com",
    description="tkinter with telerik",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests"]),
    package_data={"": ["*", "*.dll"]},
    requires=["pythonnet", "tqdm"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
