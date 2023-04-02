from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cbpi4-DependentActor',
      version='0.0.5',
      description='CraftBeerPi4 Actor Plugin to create dependencies or conditions on other actors',
      author='Alexander Vollkopf',
      author_email='avollkopf@web.de',
      url='https://github.com/PiBrewing/cbpi4-DependentActor',
      include_package_data=True,
      license='GPLv3',
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-DependentActor': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-DependentActor'],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )