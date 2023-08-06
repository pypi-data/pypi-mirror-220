from setuptools import setup, find_packages

setup(
    name='zhcevanstest',  # Replace with your desired package name
    version='1.1.6',         # Replace with your desired version number
    author='evans.zhu',
    author_email='evanszhu2001@gmail.com',
    description='A package for plotting Konrads data',
    long_description='Put a detailed description of your package here',
    long_description_content_type='text/markdown',
    packages=['zhcevanstest'],
    install_requires=['numpy', 'matplotlib'],  # Add any dependencies required by your function
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
