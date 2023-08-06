from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r",encoding='utf-8') as f:
  long_description = f.read()

setup(name='easyback', 
      version='0.1.1', 
      description='简易回测框架',
      long_description=long_description,
      author='easyback',
      author_email='915164739@qq.com',
      url='https://gitee.com/wy2629/easyback',
      install_requires=['pandas','numpy'],
      license='BSD',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
