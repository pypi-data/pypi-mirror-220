from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cfstack',
    version='0.0.3',
    description='A utility to manage CloudFormation stacks',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
            "boto3",
            "hashlib",
            "json"
    ],
    python_requires='>=3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yashdeep Suresh Shetty",
    author_email="shettyyashdeep@gmail.com",
    url="https://github.com/Yashprime1"
)
