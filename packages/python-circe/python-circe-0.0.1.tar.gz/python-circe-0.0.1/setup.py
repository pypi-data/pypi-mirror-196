from setuptools import setup, find_namespace_packages

setup(
    name='python-circe',
    description='Python wrapper for Circe',
    long_description='Python wrapper for Circe',
    long_description_content_type='text/markdown',
    version='0.0.1',
    packages=find_namespace_packages(),
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=[
        'jpype1==1.4.1',
    ]
)