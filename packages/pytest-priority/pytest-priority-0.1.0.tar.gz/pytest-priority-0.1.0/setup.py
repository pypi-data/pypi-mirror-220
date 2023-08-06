from setuptools import setup, find_packages

setup(
    name='pytest-priority',
    description='pytest plugin for add priority for tests',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    version='0.1.0',
    author='Han Zhichao',
    author_email='superhin@126.com',
    license='MIT License',
    packages=find_packages(include=['pytest_priority']),
    zip_safe=True,
    include_package_data=True,
    url='http://github.com/hanzhichao/pytest-priority',
    install_requires=['pytest', 'pytest-runner'],
    setup_requires=['pytest-runner'],
    entry_points={
        'pytest11': ['pytest-priority = pytest_priority.plugin']
    }
)
