import codecs
import os
import re
from setuptools import setup


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='scribe',
    description=('Automatically create pages and upload images to a confluence '
                 'page'),
    long_description=read('README.md'),
    version=find_version('scribe.py'),
    scripts=['scribe.py'],
    author='TrepHub',
    author_email='',
    url='https://github.com/ubergeek42/scribe',
    license='MIT License',
    install_requires=['argh=0.23.1', 'watchdog==0.6.0'],
    include_package_data=True,
)
