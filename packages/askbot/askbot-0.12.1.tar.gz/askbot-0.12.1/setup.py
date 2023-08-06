from __future__ import print_function
from setuptools import setup, find_packages
import sys
import askbot

PYTHON_VERSION_INFO = \
"""
ERROR: This version of Askbot only works with Python 3,
       if you need Askbot to work with Python 2, 
       try versions 0.10.x and earlier.
"""

if sys.version_info[0] < 3:
    print(PYTHON_VERSION_INFO)
    sys.exit(1)

setup(
    name = "askbot",
    version = askbot.get_version(),#remember to manually set this correctly
    description = 'Question and Answer forum, like StackOverflow, written in python and Django',
    packages = find_packages(exclude=['testproject']),
    author = 'Evgeny.Fadeev',
    author_email = 'evgeny.fadeev@gmail.com',
    license = 'GPLv3',
    keywords = 'forum, community, wiki, Q&A',
    entry_points = {
        'console_scripts' : [
            'askbot-setup = askbot.deployment:askbot_setup',
        ]
    },
    url = 'http://askbot.org',
    include_package_data = True,
    install_requires = askbot.REQUIREMENTS.values(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: Finnish',
        'Natural Language :: German',
        'Natural Language :: Russian',
        'Natural Language :: Serbian',
        'Natural Language :: Turkish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: JavaScript',
        'Topic :: Communications :: Usenet News',
        'Topic :: Communications :: Email :: Mailing List Servers',
        'Topic :: Communications',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    long_description_content_type='text/markdown',
    long_description = open('./README.md', 'r').read()
)

print("""**************************************************************
*                                                            *
*  Thanks for installing Askbot.                             *
*                                                            *
*  To start deploying type: askbot-setup                     *
*                                                            *
*  Please take a look at the manual http://askbot.org/doc/   *
*  And please do not hesitate to ask your questions at       *
*  at http://askbot.org/en/questions/                        *
*                                                            *
**************************************************************""")
