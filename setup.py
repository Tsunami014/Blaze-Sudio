from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "readme.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name='Blaze-Sudio',
    version='1.3.0',
    license='Apache',
    description='This is the really cool studio to create games!',
    url='https://github.com/Tsunami014/Blaze-Sudio',
    download_url='https://github.com/Tsunami014/Blaze-Sudio/archive/refs/tags/v1.2.0-alpha.tar.gz',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    author='Max Worrall',
    author_email='max.worrall@education.nsw.gov.au',
    install_requires=[
        'requests',
        'connect-markdown-renderer',
        'pygame',
        'gpt4all',
        'languagemodels',
        'noise',
        'scikit-image',
        'pyLdtk',
    ],
    keywords=['AI', 'Python', 'games'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        'Topic :: Software Development :: Build Tools',
        #"Operating System :: Unix",
        #"Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)

# Development Status options: 
# 1 - Planning
# 2 - Pre-Alpha
# 3 - Alpha
# 4 - Beta
# 5 - Production/Stable
# 6 - Mature
# 7 - Inactive
