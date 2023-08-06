from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as f:
  long_description = f.read()

setup(name='baimomcsm_api',  # 包名
      version='0.0.5',  # 版本号
      description='MCSManager API for Python (开发中)',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='BaimoQilin',
      author_email='admin@baimoqilin.top',
      url='https://github.com/Zhou-Shilin/BaimoMCSManager-API',
      install_requires=["requests"],
      license='Apache 2.0',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Topic :: Software Development :: Libraries'
      ],
      )