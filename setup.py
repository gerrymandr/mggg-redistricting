from setuptools import setup

# do not pin requirements here (constraining is OK) - if you really must, make
#    a requirements.txt file, but then you need to keep it in sync with this
#    list.
# In other words,
#
#    somedep==1.2.3    => bad
#
#    somedep>=4.5      => OK

requirements = [
    'fiona',
    'numpy',
    'pandas',
    'pysal',
    'scipy',
    'shapely',
    'matplotlib',
    'palettable',
]

setup(
    name='state-adjacency-graphs',
    version='0.1.0',
    description="computes adjacency graphs from district boundary data",
    author="Gerry Mander",
    author_email='gerrymandr@gmail.com',
    url='https://github.com/gerrymandr/state-adjacency-graphs',
    packages=['adjacency_graphs'],
    entry_points={
        'console_scripts': [
            'adjacency_graphs=adjacency_graphs.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='state-adjacency-graphs',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
