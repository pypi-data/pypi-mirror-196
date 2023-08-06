from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='zcbot_service_sdk',
    version='0.0.2',
    description='zcbot service sdk for zsodata',
    long_description=long_description,
    author='yk',
    author_email='815583442@qq.com',
    url='http://gitee.com',
    install_requires=['celery>=5.2.7', 'redis>=4.3.5'],
    python_requires=">=3.7",
    license='BSD License',
    packages=find_packages(),
    platforms=['all'],


)