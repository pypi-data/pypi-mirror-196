from setuptools import setup


def read_file(fname):
    with open(fname) as f:
        return f.read()


setup(
    name='testrail-pytest',
    description='pytest plugin for creating TestRail runs and adding results',
    version='1.0.0',
    author='Vivek Singh',
    author_email='vs.bhadauriya@live.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/II-VSB-II/pytest-testrail/',
    packages=[
        'pytest_testrail',
    ],
    package_dir={'pytest_testrail': 'pytest_testrail'},
    install_requires=[
        'pytest>=3.6',
        'requests>=2.20.0',
    ],
    include_package_data=True,
    entry_points={'pytest11': ['pytest-testrail = pytest_testrail.conftest']},
)
