
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import sys, os, glob

from const import VERSION
here = os.path.abspath(os.path.dirname(__file__))
# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

src_files = glob.glob('*.py')
src_gui_files = glob.glob('gui/*.py')
data_examples = glob.glob('example*.*') 
print( data_examples )
data_ui = glob.glob('gui/*.ui')


setup(
    name='SxTool',
    version=VERSION,
    description='Tool to manipulate SX files (S-records) such as s19 s28 and s37 files',
    long_description=long_description, 
    long_description_content_type='text/markdown',
    url='https://github.com/bluebird75/sxtool',
    license = 'BSD',
    author='Philippe Fremy',
    author_email='phil.fremy@free.fr',

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[ 
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: Qt',

        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',

        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Utilities',
    ],

    keywords='sxtool s19 s28 s37',

    packages={ 
        '.' : src_files, 
        'gui': src_gui_files,
    },

    # include_package_data=True,
    package_data={
        '': [ 'generate_ui.bat', 'README.md', 'LICENSE.txt'],
        'gui' : [ '*.ui' ],
    },

    install_requires=['pyqt5>=5.8'],
    python_requires='>=3.5',

    entry_points={
        'gui_scripts': [
            'sxtool=sxtool:main',
        ],
    },

    extras_require={},
    project_urls={},
)
