from setuptools import setup

setup(name='cbpi4-DependentActor',
      version='0.0.3',
      description='CraftBeerPi4 Actor Plugin to create dependencies or conditions on other actors',
      author='',
      author_email='avollkopf@web.de',
      url='https://github.com/PiBrewing/cbpi4-DependentActor',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-DependentActor': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-DependentActor'],
     )