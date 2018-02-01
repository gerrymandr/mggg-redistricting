from setuptools import find_packages, setup

setup(
    name='mggg_graphs',
    version='0.0.2',
    packages=find_packages(),
    description='A library for turning shapefiles into graphs for redistricting.',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Mathematicians',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=open('requirements.txt').readlines(),
    python_requires='>=2.7',
    keywords='metric geometry gerrymandering redistricting'
)
