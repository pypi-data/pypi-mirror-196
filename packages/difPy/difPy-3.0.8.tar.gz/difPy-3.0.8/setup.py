from setuptools import setup
import os

base_dir = os.path.dirname(__file__)

try:
  with open(os.path.join(base_dir, "README_pypi.md")) as f:
    long_description = f.read()
except:
  with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

exec(open('difPy/version.py').read())

setup(
  name = 'difPy',         
  packages = ['difPy'],   
  version = __version__,      
  license='MIT',        
  description = 'difPy Python Duplicate Image Finder - searches for duplicate or similar images within folders.', 
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Elise Landman',                  
  author_email = 'elisejlandman@hotmail.com', 
  url = 'https://github.com/elisemercury/Duplicate-Image-Finder', 
  download_url = 'https://github.com/elisemercury/Duplicate-Image-Finder/archive/refs/tags/v3.0.8.tar.gz',
  keywords = ['duplicate', 'image', 'finder', "similarity", "pictures"],  
  install_requires=[          
          'matplotlib',
          'numpy',
          'Pillow',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',    
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)