from setuptools import setup, find_packages

setup(
    name='bcitoolbox',  # Replace with your desired package name
    version='0.0.1.3',         # Replace with your desired version number
    author='evans.zhu',
    author_email='evanszhu2001@gmail.com',
    description='A package for Bayesian causal inference model',
    long_description='A zero-programming toolbox.',
    long_description_content_type='text/markdown',
    packages=['bcitoolbox'],
    install_requires=['numpy', 'matplotlib', 'scipy'],  # Add any dependencies required by your function
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
