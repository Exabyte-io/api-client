from setuptools import setup, find_packages

setup(
    name='exabyte-api-client',
    description='Exabyte Python Client for RESTful API',
    version='0.1.1',
    url='http://github.com/Exabyte-io/exabyte-api-client',
    author='Mohammad Mohammadi',
    author_email='mohammad@exabyte.io',
    license='Exabyte Inc.',
    packages=find_packages(),
    install_requires=[
        'mock==1.3.0',
        'requests==2.13.0',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development'
    ],
)
