from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='enigmamachine',
  version='0.0.2',
  description='A basic cryptography libary, simulating the Enigma Machine',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Tomas Rodrigues Alessi',
  author_email='tomasalessi@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='cryptography', 
  packages=find_packages(),
  install_requires=['numpy>=1.21.5'] 
)