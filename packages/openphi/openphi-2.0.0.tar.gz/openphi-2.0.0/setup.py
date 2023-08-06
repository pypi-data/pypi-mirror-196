from distutils.core import setup
setup(
  name = 'openphi',
  packages = ['openphi'],
  version = '2.0.0',
  license='MIT',
  description = 'OpenPhi, an API to access Philips iSyntax images.',
  author = 'Nita Mulliqi',
  author_email = 'mulliqi.nita@gmail.com',
  url = 'https://gitlab.com/BioimageInformaticsGroup/openphi',
  download_url = 'https://gitlab.com/BioimageInformaticsGroup/openphi/-/archive/v2.0.0/openphi-v2.0.0.tar.gz',
  keywords = ['PYTHON', 'API', 'PHILIPS', 'iSyntax', 'DIGITAL', 'PATHOLOGY'],
  install_requires=[
          'numpy>=1.18',
          'pillow>=8.0',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
  ],
)
