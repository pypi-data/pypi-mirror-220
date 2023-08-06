from setuptools import setup, find_packages

setup(
  name = 'web3r',
  version = '0.0.4',  # or '0.1.1' or whatever your next version number should be
  packages=find_packages(),
  license='MIT',
  description = 'Web3R.py is a Python wrapper that enhances the functionality of Web3.py and integrates with Etherscan\'s API.',
  author = 'Finn Castro',
  author_email = 'finnfierro@gmail.com',  # Update with your email
  url = 'https://github.com/FinnCastro/Web3R',
  download_url = 'https://github.com/FinnCastro/Web3R/archive/refs/tags/0.0.4.tar.gz',
  keywords = ['web3.py', 'Etherscan', 'Ethereum', 'Blockchain', 'API'],
  install_requires=[
          'web3',  # Assuming that your project depends on web3 and requests
          'requests',
          'pandas',
          'numpy',
          'etherscan-python',
          'tqdm'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',  # Update with the Python versions you support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
