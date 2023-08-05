# pylint: disable-msg=W0622
"""cubicweb-expense application packaging information"""

modname = 'expense'
distname = 'cubicweb-expense'

numversion = (0, 9, 5)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'Logilab'
author_email = 'contact@logilab.fr'
description = 'expense component for the CubicWeb framework'
web = 'http://www.cubicweb.org/project/%s' % distname
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]

__depends__ = {'cubicweb': '>= 3.24.0, < 3.38.0',
               'cubicweb-addressbook': '>= 1.12.1, < 1.13.0',
               'cubicweb-file': '>= 3.4.1, < 3.5.0',
               }
