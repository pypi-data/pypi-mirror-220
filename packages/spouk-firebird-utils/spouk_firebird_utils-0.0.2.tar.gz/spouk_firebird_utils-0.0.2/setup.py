from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='spouk_firebird_utils',
  version='0.0.2',
  author='spouk',
  author_email='cyberspouk@gmail.com',
  description='utils for working with firebird databases',
  long_description=readme(),
  long_description_content_type='text/markdown',
  license="MIT",
  url='https://gitlab.com/Spouk',
  packages=find_packages(),
  install_requires=['fdb>=2.0.2'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  python_requires='>=3.7'
)