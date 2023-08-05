import os
from setuptools import setup

descr = """Epilepsy seizure forecasting package"""

version = None
with open(os.path.join('pyepilepsy', '__init__.py'), 'r') as fid:
    for line in (line.strip() for line in fid):
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('\'')
            break
if version is None:
    raise RuntimeError('Could not determine version')


DISTNAME = 'pyEpilepsy'
DESCRIPTION = descr
MAINTAINER = 'Etienne de Montalivet'
MAINTAINER_EMAIL = 'etienne.demontalivet@protonmail.com'
LICENSE = 'BSD (3-clause)'
DOWNLOAD_URL = 'https://github.com/etiennedemontalivet/pyEpilepsy.git'
VERSION = version


if __name__ == "__main__":
    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          long_description=open('README.rst').read(),
          long_description_content_type='text/x-rst',
          classifiers=['Intended Audience :: Science/Research',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved',
                       'Programming Language :: Python',
                       'Topic :: Software Development',
                       'Topic :: Scientific/Engineering',
                       'Operating System :: Microsoft :: Windows',
                       'Operating System :: POSIX',
                       'Operating System :: Unix',
                       'Operating System :: MacOS',
                       'Programming Language :: Python :: 3',
                       ],
          platforms='any',
          python_requires='>=3.6',
          packages=['pyepilepsy'],
          install_requires=['numpy', 'pandas'],
          )