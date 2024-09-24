from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

VERSION = '1.0.1'

setup(
    name='py_lead_generation',
    version=VERSION,
    license = 'MIT',
    author='Madi-S (Madi Shaiken)',
    author_email='<khovansky99@gmail.com>',
    description='Lead generation scripts',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Madi-S/Lead-Generation',
    packages=find_packages(),
    install_requires=['playwright', 'beautifulsoup4', 'geopy'],
    python_requires='>=3.10',
    keywords=['python', 'lead generation', 'web automation',
              'playwright', 'google maps', 'yelp'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.10',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ]
)
