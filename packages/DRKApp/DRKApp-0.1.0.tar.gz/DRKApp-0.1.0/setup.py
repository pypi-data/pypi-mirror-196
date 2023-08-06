# Create a setup.py file for the drkApp package

from setuptools import setup


setup(
    name='DRKApp',
    version='0.1.0',
    description="A Python package to access the DRK APP API",
    url='https://github.com/iamrraj/Mattr_lib',
    author="Rahul Raj",
    author_email="rajr97333@gmail.com",
    license='MIT',
    packages=['DRKApp'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='DRK APP API',


)
