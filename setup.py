from setuptools import setup

setup(name='cbpi4-DependentActor',
      version='0.0.2',
      description='CraftBeerPi Plugin',
      author='',
      author_email='',
      url='',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-DependentActor': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-DependentActor'],
     )