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

import re
import textwrap

import mistune


class TWBlockLexer(mistune.BlockLexer):
    """Text Wrap Block lexer for block grammar."""

    def __init__(self, rules=None, **kwargs):
        super(TWBlockLexer, self).__init__(rules, **kwargs)

        # from mistune
        self._key_pattern = re.compile(r'\s+')

    # from mistune
    def _keyify(self, key):
        key = mistune.escape(key.lower(), quote=True)
        return self._key_pattern.sub(' ', key)

    def parse_block_code(self, m):
        self.tokens.append({
            'type': 'code',
            'lang': None,
            'text': m.group(0),
        })

    def parse_fences(self, m):
        self.tokens.append({
            'type': 'code',
            'lang': None,
            'text': m.group(0),
        })

    def parse_heading(self, m):
        self.tokens.append({
            'type': 'heading',
            'level': len(m.group(1)),
            'text': m.group(0),
        })

    def parse_lheading(self, m):
        """Parse setext heading."""
        self.tokens.append({
            'type': 'heading',
            'level': 1 if m.group(2) == '=' else 2,
            'text': m.group(0),
        })

    def parse_hrule(self, m):
        self.tokens.append({
            'type': 'hrule',
            'text': m.group(0)
            })

    def _process_list_item(self, cap, bull):
        cap = self.rules.list_item.findall(cap)

        _next = False
        length = len(cap)

        for i in range(length):
            item = cap[i][0]

            # slurp and remove the bullet
            space = len(item)
            bullet = ''
            bm = self.rules.list_bullet.match(item)
            if bm:
                bullet = bm.group(0)

            item = self.rules.list_bullet.sub('', item)

            # outdent
            if '\n ' in item:
                space = space - len(item)
                pattern = re.compile(r'^ {1,%d}' % space, flags=re.M)
                item = pattern.sub('', item)

            # determine whether item is loose or not
            loose = _next
            if not loose and re.search(r'\n\n(?!\s*$)', item):
                loose = True

            rest = len(item)
            if i != length - 1 and rest:
                _next = item[rest-1] == '\n'
                if not loose:
                    loose = _next

            if loose:
                t = 'loose_item_start'
            else:
                t = 'list_item_start'

            self.tokens.append({
                'type': t,
                'text': bullet,
                'spaces': len(bullet)
                })

            # recurse
            self.parse(item, self.list_rules)

            self.tokens.append({
                'type': 'list_item_end',
                'spaces': len(bullet)
                })


class TWInlineLexer(mistune.InlineLexer):
    """Text Wrap Inline level lexer for inline gramars."""

    def __init__(self, renderer, rules=None, **kwargs):
        super(TWInlineLexer, self).__init__(renderer, rules, **kwargs)

        # No inline rules.
        self.default_rules = []

    def output(self, text, rules=None):
        # Don't parse inline text.
        return text


class TWRenderer(mistune.Renderer):
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


class TWMarkdown(mistune.Markdown):
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
