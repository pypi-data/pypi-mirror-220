from setuptools import setup, find_packages

setup(
    name='mbforbes_python_utils',
    version='0.4.0',
    author='Maxwell Forbes',
    description="Some tiny python utils so I can be lazier.",
    url="https://github.com/mbforbes/python-utils",
    license='MIT',
    packages=find_packages(),
    package_data={"mbforbes_python_utils": ["py.typed"]},
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.9',
)
