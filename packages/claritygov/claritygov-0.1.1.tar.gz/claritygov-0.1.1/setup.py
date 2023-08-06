from setuptools import setup, find_packages

setup(
    name='claritygov',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'pytest==7.4.0'
    ],
    keywords=['claritygov', 'clarityapi', 'government', 'transparency'],
    license='Creative Commons Attribution 4.0 International Public License',
    description='Python API Client for ClarityGov, a free public developer API for accessing government legislative data in a standardized format.',
    long_description=open('README.md').read(),
    author='ClarityGov',
    download_url='https://github.com/ianmcvann/ClarityGovClient/archive/refs/tags/v0.1.1.tar.gz',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3'
    ]
)