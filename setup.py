import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="london-unified-prayer-times",
    version="0.0.1",
    author="sshaikh",
    author_email="sshaikh@users.noreply.github.com",
    description="A library for retrieving the London Unified Prayer Timetable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sshaikh/london-unified-prayer-timetable",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
