# -*- coding: utf-8 -*-
#
#   Copyright © 2018 rsiddharth <s@ricketyspace.net>.
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
        self._block_quote_leading_pattern = re.compile(r'^ *> ?', flags=re.M)
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

    def parse_block_quote(self, m):
        # slurp and clean leading >
        quote = ''
        qm = self._block_quote_leading_pattern.match(m.group(0))
        if qm:
            quote = qm.group(0)

        cap = self._block_quote_leading_pattern.sub('', m.group(0))

        self.tokens.append({
            'type': 'block_quote_start',
            'text': quote,
            'spaces': len(quote)
            })
        self.parse(cap)
        self.tokens.append({
            'type': 'block_quote_end',
            'spaces': len(quote)
            })

    def parse_def_links(self, m):
        key = self._keyify(m.group(1))
        self.def_links[key] = {
            'link': m.group(2),
            'title': m.group(3),
        }
        self.tokens.append({
            'type': 'def_links',
            'text': m.group(0)
            })

    def parse_def_footnotes(self, m):
        key = self._keyify(m.group(1))
        if key in self.def_footnotes:
            # footnote is already defined
            return

        self.def_footnotes[key] = 0

        text = m.group(2)
        multiline = False
        spaces = 0
        if '\n' in text:
            multiline = True
            lines = text.split('\n')
            whitespace = None
            for line in lines[1:]:
                space = len(line) - len(line.lstrip())
                if space and (not whitespace or space < whitespace):
                    whitespace = space
            newlines = [lines[0]]
            for line in lines[1:]:
                newlines.append(line[whitespace:])
            text = '\n'.join(newlines)

            if whitespace:
                spaces = whitespace

        self.tokens.append({
            'type': 'footnote_start',
            'key': key,
            'multiline': multiline,
            'spaces': spaces
        })

        self.parse(text, self.footnote_rules)

        self.tokens.append({
            'type': 'footnote_end',
            'key': key,
            'spaces': spaces
        })


class TWInlineLexer(mistune.InlineLexer):
    """Text Wrap Inline level lexer for inline gramars."""

    def __init__(self, renderer, rules=None, **kwargs):
        super(TWInlineLexer, self).__init__(renderer, rules, **kwargs)

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

    def tw_get(self, attr):
        """Get attribute from the local textwrap.TextWrapper instance.
        """
        return getattr(self.tw, attr, None)


    def tw_set(self, **kwargs):
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
        self.tw_set(**kwargs)
        return self.tw.fill(text)

    def block_code(self, code, lang=None):
        out = '{}'.format(code)
        out = textwrap.indent(out, self.tw_get('initial_indent'),
                              lambda line: True)
        return out

    def block_quote(self,  text):
        out = '{}'.format(text.rstrip('>\n'))
        return out

    def paragraph(self, text):
        out = self._tw_fill(text)
        out = '{}\n{}\n'.format(out, self.tw_get('initial_indent').strip())
        return out


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

    def _clean_ts(self, lines):
        out = ''

        for line in lines.split('\n'):
            out += line.rstrip() + '\n'

        return out

    def parse(self, text):
        out = super(TWMarkdown, self).parse(text)

        # Remove trailing spaces from all lines.
        out = self._clean_ts(out)

        # Add newline at the end.
        return '{}\n'.format(out.strip('\n'))


def main():
    print('USAGE: md_tw 72 file.md file2.md [...]')
