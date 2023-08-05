from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='latteOne',
  version='0.0.5',
  description='simple classification algorithms',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sebinmon Vr ',
  author_email='nthn8777@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='latte_classifier', 
  packages=find_packages(),
  install_requires=['numpy','matplotlib','sklearn'] 
)