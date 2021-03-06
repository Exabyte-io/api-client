from setuptools import setup, find_packages

with open('./README.md', 'r') as f:
    long_description = f.read()

setup(
    name='exabyte-api-client',
    setup_requires=['setuptools_scm'],
    use_scm_version={
        'version_scheme': 'post-release',
    },
    description='Exabyte Python Client for RESTful API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/Exabyte-io/exabyte-api-client',
    author='Exabyte Inc.',
    author_email='info@exabyte.io',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'requests==2.20.1'
    ],
    extras_require={
        "test": [
            "coverage[toml]>=5.3",
            "mock>=1.3.0",
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: Apache Software License'
    ],
)
