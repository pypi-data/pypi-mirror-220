from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='smartpyml',          
    version='0.1.0',              
    author='srikresna',
    author_email='srikresna383@gmail.com',
    description='smartpyml: A Comprehensive Machine Learning Library',
    long_description='''smartpyml is a comprehensive machine learning library that empowers developers and data scientists to easily apply classical machine learning algorithms and time series analysis techniques. It provides a collection of user-friendly functions and tools for data preprocessing, model training, evaluation, and prediction, making it suitable for both beginners and experienced practitioners in the field of data science and artificial intelligence.

Main Features:
- A wide range of classical machine learning algorithms
- Time series analysis and forecasting capabilities
- User-friendly interfaces for easy implementation
- Data preprocessing utilities for feature engineering
- Model evaluation and performance metrics
- Support for both numerical and categorical data

- WARNING: This library is still in development and may contain bugs.
For more information and examples, visit the GitHub repository: https://github.com/srikresna/smartpyml''',
    long_description_content_type='text/markdown',
    url='https://github.com/srikresna/smartpyml', 
    packages=find_packages(),      
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='machine learning, data science, automl, ai',
    install_requires=required_packages,
)
