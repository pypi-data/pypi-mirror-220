from os import path

from setuptools import find_packages, setup

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering :: Mathematics',
]

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xmcda',
    version='0.3',
    description='Read, write and manipulate XMCDA objects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sébastien Bigaret',
    author_email='sebastien.bigaret@telecom-bretagne.eu',
    classifiers=classifiers,
    install_requires=('lxml', 'python-dateutil'),
    python_requires='>=3.6',
    packages=find_packages(exclude=['tests*']),
    # url=''
    package_dir={'xmcda': 'xmcda'},
    package_data={'xmcda': ['xsd/*']},
    test_suite='tests',
    project_urls={
        'Source': 'https://gitlab.com/sbigaret/xmcda-python',
    },
)
