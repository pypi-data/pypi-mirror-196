from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='cryptolibrary',
  version='0.0.1',
  description='Cryptography libary',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Enzo Quental',
  author_email='ezq2202@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='crypto', 
  packages=find_packages(),
  install_requires=['numpy>=1.21.5'] 
)