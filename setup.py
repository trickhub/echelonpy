from setuptools import find_packages
from setuptools import setup

MAJOR_VERSION = '0'
MINOR_VERSION = '1'
MICRO_VERSION = '0'
VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION)

setup(name='echelonpy',
      version=VERSION,
      description="Converts Schwinn MPower Echelon csv output to Garmin compatible tcx",
      author='Tom Rickards',
      url='https://github.com/trickhub/echelonpy',
      author_email='tomrickards@gmail.com',
      install_requires=[
          'lxml',
      ],
      entry_points={
          'console_scripts': ['echelonpy = echelonpy.__main__:main']
      },
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: Microsoft',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
      ],
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      platforms='any')
