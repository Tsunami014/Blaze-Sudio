from setuptools import setup, find_packages

setup(
    name='graphics',
    version='1.3.0',
    license='Apache',
    description='This is the graphics portion of https://github.com/Tsunami014/Blaze-Sudio',
    url='https://github.com/Tsunami014/Blaze-Sudio',
    long_description_content_type="text/markdown",
    long_description="For more details see https://github.com/Tsunami014/Blaze-Sudio",
    packages=find_packages(),
    author='Max Worrall',
    author_email='max.worrall@education.nsw.gov.au',
    install_requires=[
        'requests',
        'pygame',
    ],
    keywords=['graphics', 'Python'],
    classifiers=[
        "Development Status :: 4 - Beta",
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
