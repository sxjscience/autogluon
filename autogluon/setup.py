#!/usr/bin/env python
import os
import shutil
import subprocess
import codecs
import os.path

from setuptools import setup, find_packages, find_namespace_packages

cwd = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join('..', 'VERSION')) as version_file:
    version = version_file.read().strip()

"""
This namespace package is added to enable `pip install autogluon` which will install the full AutoGluon package with all the dependencies included.
For local installations, other modules must be built separately via the `full_install.sh` script. 
This `setup.py` file will NOT install the full autogluon package and all its dependencies.

To release a new stable version on PyPi, simply tag the release on github, and the Github CI will automatically publish 
a new stable version to PyPi using the configurations in .github/workflows/pypi_release.yml . 
You need to increase the version number after stable release, so that the nightly pypi can work properly.
"""
try:
    if not os.getenv('RELEASE'):
        from datetime import date
        today = date.today()
        day = today.strftime("b%Y%m%d")
        version += day
except Exception:
    pass

def create_version_file():
    global version, cwd
    print('-- Building version ' + version)
    version_path = os.path.join(cwd, 'src', 'autogluon', 'version.py')
    with open(version_path, 'w') as f:
        f.write('"""This is autogluon version file."""\n')
        f.write("__version__ = '{}'\n".format(version))


long_description = open(os.path.join('..', 'README.md')).read()

MIN_PYTHON_VERSION = '>=3.6.*'

requirements = [
    'Pillow<=6.2.1',
    'numpy>=1.16.0',
    'scipy>=1.3.3',
    'cython',
    'tornado>=5.0.1',
    'requests',
    'matplotlib',
    'tqdm>=4.38.0',
    'paramiko>=2.4',
    'dask>=2.6.0',
    'cryptography>=2.8',
    'distributed>=2.6.0',
    'ConfigSpace<=0.4.10',
    'gluoncv>=0.5.0,<1.0',
    'graphviz<0.9.0,>=0.8.1',
    'fastparquet==0.4.1',
    'scikit-optimize',
    'catboost>=0.23.0,<0.25',
    'pyarrow<=1.0.0',
    'boto3',
    'lightgbm>=3.0,<4.0',
    'pandas>=1.0.0,<2.0',
    'psutil>=5.0.0,<=5.7.0',  # TODO: psutil 5.7.1/5.7.2 has non-deterministic error on CI doc build -  ImportError: cannot import name '_psutil_linux' from 'psutil'
    'scikit-learn>=0.22.0,<0.24',
    'networkx>=2.3,<3.0',
    'autogluon.core',
    'autogluon.tabular',
    'autogluon.mxnet',
    'autogluon.extra',
    'autogluon.text',
    'autogluon.vision'
]

test_requirements = [
    'pytest'
]

if __name__ == '__main__':
    create_version_file()
    setup(
        # Metadata
        name='autogluon',
        version=version,
        author='AutoGluon Community',
        url='https://github.com/awslabs/autogluon',
        description='AutoML Toolkit with MXNet Gluon',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='Apache',

        # Package info
        packages=find_packages('src'),
        package_dir={'': 'src'},
        namespace_packages=["autogluon"],
        zip_safe=True,
        include_package_data=True,
        install_requires=requirements + test_requirements,
        python_requires=MIN_PYTHON_VERSION,
        package_data={'autogluon': [
            'LICENSE',
        ]},
        entry_points={
        },
    )
