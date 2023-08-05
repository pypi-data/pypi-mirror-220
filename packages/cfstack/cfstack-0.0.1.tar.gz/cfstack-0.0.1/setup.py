from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cfstack',
    version='0.0.1',
    description='A utility to manage CloudFormation stacks',
    py_modules=["main"],
    package_dir={'': 'src/cfstack'},
    extras_require={
        "dev": [
            "boto3",
            "hashlib",
            "json"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yashdeep Suresh Shetty",
    author_email="shettyyashdeep@gmail.com",
    url="https://github.com/Yashprime1"
)
