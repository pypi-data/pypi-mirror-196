from setuptools import setup

setup(
    name='lisql',
    version='2.0.4',
    py_modules=['lisql'],
    description='A Python package for simplifying the interaction with MySQL databases.',
    author='Ali Ahammad',
    author_email='aliahammad0812@outlook.com',
    url='https://github.com/li812/lisql',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'mysql-connector-python',
        'mysql'
    ],
)