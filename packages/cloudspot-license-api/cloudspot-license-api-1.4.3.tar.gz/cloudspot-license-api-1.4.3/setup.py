from setuptools import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'cloudspot-license-api',         
  packages=['cloudspotlicense', 'cloudspotlicense.models', 'cloudspotlicense.constants', 'cloudspotlicense.endpoints'],
  version = '1.4.3',
  license='GPL-3.0-or-later',
  description = 'Wrapper for the Cloudspot License API endpoints',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Alexander Schillemans',
  author_email = 'alexander.schillemans@lhs.global',
  url = 'https://github.com/Ecosy-EU/cloudspot-license-api',
  download_url = 'https://github.com/Ecosy-EU/cloudspot-license-api/archive/refs/tags/1.4.3.tar.gz',
  keywords = ['cloudspot'],
  install_requires=[
          'requests',
          'python-dateutil',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3.6',
  ],
)