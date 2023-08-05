from setuptools import setup

setup(
    name="VikScraper",
    version='0.1.0',
    description='Tool for Scraping PDF files given Google Query',
    author='Vikram Nagapudi',
    author_email='vikram@concentric.ai',
    license='BSD 2-clause',
    packages=['VikScraper'],
    url='https://github.com/vik135/VikScraper',
    install_requires=['requests', 'requests_html', 'urllib3', 'numpy', 'sklearn',
                      'pandas', 'duckduckgo_search', 'gensim', 'nltk', 'urllib', 'distance'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)