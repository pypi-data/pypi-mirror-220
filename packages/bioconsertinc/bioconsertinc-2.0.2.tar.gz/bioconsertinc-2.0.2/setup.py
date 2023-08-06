from setuptools import setup
from distutils.extension import Extension


def get_numpy_include_dirs():
    import numpy
    return [numpy.get_include()]


setup(name='bioconsertinc',
      version='2.0.2',
      description='BioConsert, c implementation',
      url='https://github.com/pierreandrieu/bioconsertinc',
      long_description='BioConsert algorithm, c implementation',
      author='Pierre Andrieu',
      author_email='pierre.andrieu@lilo.org',
      license='MIT',
      ext_modules=[Extension("bioconsertinc", ["bioconsertinc.c"], include_dirs=get_numpy_include_dirs())],
      python_requires='>=3.8',
      zip_safe=False,
      install_requires=['numpy>=1.24.0'],
      )
