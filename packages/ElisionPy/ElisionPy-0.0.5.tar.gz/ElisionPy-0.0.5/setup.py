from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='ElisionPy',
  version='0.0.5',
  author='Ginji',
  author_email='bfire1999@gmail.com',
  description='This module is under development!',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Ginji-Fox/ElisionPy',
  packages=find_packages(),
  install_requires=['requests>=2.25.1', 'datetime>=5.2'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='ElisionPy Elision',
  project_urls={
    'Documentation': 'https://github.com/Ginji-Fox/ElisionPy'
  },
  python_requires='>=3.7'
)