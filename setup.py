from setuptools import setup, find_packages

with open('readme.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='Blaze-Sudio',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.2.0',
    license='Apache',
    description='This is the really cool studio to create games!',
    author='Max Worrall',
    author_email='max.worrall@education.nsw.gov.au',
    url='https://github.com/Tsunami014/Blaze-Sudio',
    download_url='https://github.com/Tsunami014/Blaze-Sudio/archive/refs/tags/v1.1.0-alpha.tar.gz',
    keywords=['AI', 'Python', 'games'],
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
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',
        # 'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 3.10',
    ],
)
