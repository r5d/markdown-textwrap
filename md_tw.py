# -*- coding: utf-8 -*-
#
#   Copyright © 2017 markdown-textwrap contributors.
#
#    This file is part of markdown-textwrap.
#
#   markdown-textwrap is free software: you can redistribute it
#   and/or modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation, either version 3 of
#   the License, or (at your option) any later version.
#
#   markdown-textwrap is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#   See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with markdown-textwrap (see COPYING).  If not, see
#   <http://www.gnu.org/licenses/>.

import textwrap

from mistune import BlockLexer, InlineLexer, Renderer, Markdown


class TWBlockLexer(BlockLexer):
    """Text Wrap Block level lexer for block grammars."""

    def __init__(self, rules=None, **kwargs):
        super(TWBlockLexer, self).__init__(rules, **kwargs)

        self.default_rules = ['paragraph', 'text']


class TWInlineLexer(InlineLexer):
    """Text Wrap Inline level lexer for inline gramars."""

    def __init__(self, renderer, rules=None, **kwargs):
        super(TWInlineLexer, self).__init__(renderer, rules, **kwargs)

        # No inline rules.
        self.default_rules = []

    def output(self, text, rules=None):
        # Don't parse inline text.
        return text


class TWRenderer(Renderer):
    """Text Wrap Renderer."""

    def __init__(self, **kwargs):
        super(TWRenderer, self).__init__(**kwargs)

        # Initalize textwrap.TextWrapper class
        self.tw = textwrap.TextWrapper(
            width=kwargs.get('tw_width', 72)
        )


    def _tw_set_options(self, **kwargs):
        """
        Set options for the local textwrap.TextWrapper instance.
        """
        # Recognized options.
        opts = [
            'width',
            'initial_indent',
            'subsequent_indent',
            'drop_whitespace'
        ]

        for opt, val in kwargs.items():
            if not opt in opts:
                continue

            # Set option
            setattr(self.tw, opt, val)


    def _tw_fill(self, text, **kwargs):
        """Wrap text.
        """
        self._tw_set_options(**kwargs)
        return self.tw.fill(text)


    def paragraph(self, text):
        return '\n{}\n'.format(self._tw_fill(text))


class TWMarkdown(Markdown):
    """Text Wrap Markdown parser.
    """

    def __init__(self, **kwargs):
        renderer = TWRenderer(**kwargs)

        super(TWMarkdown, self).__init__(
            renderer,
            TWInlineLexer,
            TWBlockLexer
        )

    def parse(self, text):
        out = super(TWMarkdown, self).parse(text)

        # Strip newline at the beginning.
        return out.lstrip('\n')


def main():
    print('USAGE: md_tw 72 file.md file2.md [...]')
