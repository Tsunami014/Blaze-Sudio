from distutils.core import setup
# TODO: finish this
setup(
  name = 'Blaze-Sudio',         # How you named your package folder
  packages = ['Blaze-Sudio'],   # Chose the same as "name"
  version = '1.1.0',      # Start with a small number and increase it with every change you make
  license='Apache',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is the really cool studio to create games!',   # Give a short description about your library
  author = 'Max Worrall',                   # Type in your name
  author_email = 'max.worrall@education.nsw.gov.au',      # Type in your E-Mail
  url = 'https://github.com/Tsunami014/Blaze-Sudio',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Tsunami014/Blaze-Sudio/archive/refs/tags/v1.1.0-alpha.tar.gz',
  keywords = ['AI', 'Python', 'games'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
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
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    #'Topic :: Software Development :: Build Tools',
    #'License :: OSI Approved :: MIT License',   # Again, pick a license
    #'Programming Language :: Python :: 3.10',      # Specify which pyhton versions that you want to support
  ],
)