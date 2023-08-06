from distutils.core import setup
setup(
  name = 'openaiclind',         # How you named your package folder (MyLib)
  packages = ['openaiclind'],   # Chose the same as "name"
  version = '3897',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A python cli client for openai powered chatbot made in India (***********make sure to paste your api key in a file called 1.txt in same folder as driver code*********) pip3 install pycryptodome and pip3 install openai from openaiclind import *',   # Give a short description about your library
  author = 'Neelanjan Manna',                   # Type in your name
  author_email = 'neelanjanmanna2021@gmail.com',      # Type in your E-Mail
  url = 'https://www.linkedin.com/in/neelanjanmanna/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.11',
  ],
)