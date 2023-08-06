from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='linmapper',
  version='0.0.9',
  description='linmapper is a Python package that allows users to transform vertices of complex numbers from one plane (Z) to another plane (f(Z)).',
  long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Supratim Das',
  author_email='supratim0707@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['calculator','linear', 'complex', 'number', 'mapping', 'supratim', 'das'],
  packages=find_packages(),
  install_requires=['numpy'] 
)