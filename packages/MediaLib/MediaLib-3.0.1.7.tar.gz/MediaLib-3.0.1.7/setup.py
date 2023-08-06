from setuptools import setup, find_packages


setup(
    name='MediaLib',
    version='3.0.1.7',
    license='MIT',
    author="Jingyun Wang",
    description="The first cut-down Python library that simplifies multimedia programming.",
    author_email='jingyun.wang@durham.ac.uk',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='http://medialib.club',
    keywords='Multimedia',
    install_requires=[
          'pygame',
      ],

)
