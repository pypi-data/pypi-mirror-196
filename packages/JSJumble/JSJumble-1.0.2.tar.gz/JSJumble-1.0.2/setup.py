from setuptools import setup, find_packages
import os

with open('./requirement.txt') as f:
  required = f.read().splitlines()
  
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Information Technology',
  'Operating System :: Unix',
  'Operating System :: MacOS :: MacOS X',
  'Operating System :: Microsoft :: Windows',
  'License :: OSI Approved :: GNU General Public License (GPL)',
  'Programming Language :: Python :: 3.6'
]

setup(
  name='JSJumble',
  version='1.0.2',
  description='Tool for obfuscating, compressing Javascript, and collecting static files.',
  long_description=open('pypi.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/GoodDay360/JSJumble',  
  author='GoodDay360',
  author_email='istartgame31@gmail.com',
  license='GNU General Public License (GPL)', 
  classifiers=classifiers,
  keywords=['JSJumble','library','module','javascript','compress','obfuscator','obfuscate','static','collect','server'], 
  packages=find_packages(exclude=[]),
  install_requires=required,
)