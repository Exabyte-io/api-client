from setuptools import setup, find_packages

setup(
    name='exabyte-api-client',
    description='Exabyte Python Client for RESTful API',
    version='1.0.0',
    url='http://github.com/Exabyte-io/exabyte-api-client',
    author='Exabyte Inc.',
    author_email='info@exabyte.io',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'mock==1.3.0',
        'requests==2.20.1'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: Apache Software License'
    ],
)
