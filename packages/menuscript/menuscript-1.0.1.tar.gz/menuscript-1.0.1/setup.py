import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="menuscript",
    version="1.0.1",
    author="Mr. Robot",
    author_email="alertsontwitter@gmail.com",
    description="A menu-based script generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AIMadeScripts/createmenus",
    py_modules=["menuscript"],
    entry_points={
        "console_scripts": [
            "menuscript=menuscript:create_script"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
