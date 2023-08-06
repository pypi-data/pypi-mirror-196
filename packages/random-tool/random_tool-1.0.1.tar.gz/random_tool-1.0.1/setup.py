from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='random_tool',  # 包名
      version='1.0.1',  # 版本号
      description='encrypt basic openssl',
      long_description_content_type="text/markdown",
      long_description=long_description,
      author='zhang peng',
      author_email='siburuxue@gmail.com',
      url='https://github.com/siburuxue',
      install_requires=[],
      license='Apache-2.0 License',
      packages=find_packages(),
      platforms=["all"],
      )
