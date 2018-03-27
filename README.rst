markdown-textwrap
=================

Petite program for text wrapping markdown_ documents.

.. _markdown: https://daringfireball.net/projects/markdown

install
-------

::

   pip3 install markdown-textwrap


usage
-----

::

  # Wrap markdown document to 66 characters.

  $ md-tw -w 66 path/to/doc.md > path/to/doc-wrapped.md

  # Wrap markdown document to 42 characters.

  $ md-tw -w 42 path/to/doc.md > path/to/doc-wrapped.md

caveats
-------

* Sentences will always be separated by a single space.
* Markdown documents with tables / task lists are not supported.


source
------

::

   git clone git://git.ricketyspace.net/markdown-textwrap.git

license
-------

Under `GNU General Public License version 3 or later`__.

.. _gplv3: https://www.gnu.org/licenses/gpl-3.0-standalone.html
__ gplv3_


help
----

Ping rsiddharth <s@ricketyspace.net>.
