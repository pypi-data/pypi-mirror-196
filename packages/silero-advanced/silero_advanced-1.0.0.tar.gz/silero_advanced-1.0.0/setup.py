from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()

setup(
  name='silero_advanced',
  version='1.0.0',
  author='FeeFort',
  author_email='bikov22022006@gmail.com',
  description='Silero-Advanced - это улучшенный модуль Silero.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/FeeFort/silero-advanced',
  packages=find_packages(),
  package_data={
    'silero_advanced': ['numText.py']
  },
  install_requires=['sounddevice>=0.4.5', 'torch>=1.13.1'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python silero',
  project_urls={
    'Documentation': 'https://github.com/FeeFort/silero-advanced'
  },
  python_requires='>=3.7'
)