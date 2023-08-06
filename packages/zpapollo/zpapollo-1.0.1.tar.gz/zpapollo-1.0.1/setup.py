# encoding: utf-8
"""
pyapollo 常用工具包


"""
from setuptools import setup, find_packages
import apollo

SHORT = u'zpapollo'

setup(
    name='zpapollo',
    version=apollo.__version__,
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    url='https://github.com/',
    author=apollo.__author__,
    author_email='2907872121@qq.com',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    package_data={'': ['*.py', '*.pyc']},
    zip_safe=False,
    platforms='any',

    description=SHORT,
    long_description=__doc__,
)
