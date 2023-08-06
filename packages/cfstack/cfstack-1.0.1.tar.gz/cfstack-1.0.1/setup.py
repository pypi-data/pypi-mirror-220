from setuptools import setup,find_packages

with open("src/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cfstack',
    version='1.0.1',
    description='A utility to manage CloudFormation stacks',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
            "boto3"
    ],
    python_requires='>=3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yashdeep Suresh Shetty",
    author_email="shettyyashdeep@gmail.com",
    url="https://github.com/Yashprime1"
)
