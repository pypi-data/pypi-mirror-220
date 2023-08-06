import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pydiff-planetarium-assignment',
    version='0.0.5',
    author='channprj',
    author_email='chann@chann.dev',
    description='Simple implementation of unix diff',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/planetarium/take-home-2023-channprj',
    project_urls={
        'Bug Tracker':
        'https://github.com/planetarium/take-home-2023-channprj/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.8',
)
