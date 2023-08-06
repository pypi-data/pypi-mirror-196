from setuptools import setup, find_namespace_packages


setup(
    name='python-circe',
    description='Python wrapper for Circe',
    long_description='Python wrapper for Circe',
    long_description_content_type='text/markdown',
    version='0.0.2',
    packages=find_namespace_packages(),
    include_package_data=True,
    package_data={
        'circe': ['*.jar', '*.json'],
    },
    python_requires='>=3.9',
    install_requires=[
        'jpype1==1.4.1',
    ]
)
