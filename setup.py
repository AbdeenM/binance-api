import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='binance-spot',
    version='0.0.1',
    author='Abdeen Mohamed, Tarun ',
    author_email='abdeen.mohamed@outlook.com, ',
    description='A python library that implements the Binance Exchange REST API and Web socket communication.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbdeenM/binance-spot',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)