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

import os
import shutil
import tempfile
import textwrap

from mistune import Renderer
from nose import tools as nose_tools
from pkg_resources import resource_string, resource_filename

from md_tw import TWBlockLexer, TWInlineLexer, TWRenderer, TWMarkdown

def _get_data(f):
    rs = resource_string(__name__, '/'.join(['data', f]))
    return rs.decode()


def _get_data_path(f):
    return resource_filename(__name__, '/'.join(['data', f]))


class TestTWBlockLexer(object):

    def setup(self):
        self.bl = TWBlockLexer()

    def _parse(self, file_):
        txt = _get_data(file_)
        return self.bl.parse(txt)

    def _validate(self, tokens, type_, expected):
        for token in tokens:
            if token['type'] == type_:
                nose_tools.assert_equal(token['text'], expected.pop(0))

    def test_parse_block_code(self):
        tokens = self._parse('blexer-block-code.md')

        expected_bc = [
            '    $ echo \'Zap!\'\n    $ rm -rf /\n\n',
            '    $ :(){:|:&};:\n\n'
            ]
        self._validate(tokens, 'code', expected_bc)

    def test_parse_fences(self):
        tokens = self._parse('blexer-fences.md')

        expected_fences = [
            '```bash\n$ echo \'Zap!\'\n$ rm -rf /\n```\n',
            '```bash\n$ :(){:|:&};:\n```\n'
            ]

        self._validate(tokens, 'code', expected_fences)

    def test_parse_heading(self):
        tokens = self._parse('blexer-heading.md')

        expected_hs = [
            '# Milky Chance\n\n',
            '## Flashed\n\n',
            '### Junk Mind\n\n',
            ]

        self._validate(tokens, 'heading', expected_hs)

    def test_parse_lheading(self):
        tokens = self._parse('blexer-lheading.md')

        expected_lhs = [
            'Milky Chance\n============\n\n',
            'Flashed\n-------\n\n',
            '### Junk Mind\n\n',
            ]

        self._validate(tokens, 'heading', expected_lhs)

    def test_parse_hrule(self):
        tokens = self._parse('blexer-hrules.md')

        expected_hrs = [
            '* * *\n\n',
            '***\n\n',
            '*****\n\n',
            '- - -\n\n',
            '---------------------------------------\n\n'
            ]

        self._validate(tokens, 'hrule', expected_hrs)

    def test_parse_list_block(self):
        tokens = self._parse('blexer-lists.md')

        def process(tokens):
            token = tokens.pop(0)
            while token:
                type_ = token['type']

                expected_token = None
                if type_ in expected:
                    expected_token = expected[type_].pop(0)

                validate(token, expected_token)

                if type_ == 'list_end':
                    break
                else:
                    token = tokens.pop(0)

            return tokens

        def validate(token, expected_token=None):
            type_ = token['type']

            if type_ == 'list_item_start':
                assert 'text' in token
                assert 'spaces' in token
            elif type_ == 'list_item_end':
                assert 'spaces' in token

            if not expected_token:
                return

            if 'text' in token:
                nose_tools.assert_equal(token['text'], expected_token['text'])
            if 'spaces' in token:
                nose_tools.assert_equal(token['spaces'], expected_token['spaces'])

            return

        # test list 1
        expected = {
            'list_item_start': [
                {'text': '+   ', 'spaces': 4},
                {'text': '+   ', 'spaces': 4},
                {'text': '+   ', 'spaces': 4}
                ],
            'text': [
                {'text': 'Re: Your Brains'},
                {'text': 'Shop Vac'},
                {'text': 'Flickr'},
                ],
            'list_item_end': [
                {'spaces': 4},
                {'spaces': 4},
                {'spaces': 4}
                ]
            }
        tokens = process(tokens)

        # test list 2
        expected = {
            'list_item_start': [
                {'text': '1.  ', 'spaces': 4},
                {'text': '2.  ', 'spaces': 4},
                {'text': '3.  ', 'spaces': 4}
                ],
            'text': [
                {'text': 'First of May'},
                {'text': 'You Ruined Everything'},
                {'text': 'Sucker Punch'},
                ],
            'list_item_end': [
                {'spaces': 4},
                {'spaces': 4},
                {'spaces': 4}
                ]
            }
        token = process(tokens)

        # test list 3
        expected = {
            'list_item_start': [
                {'text': '*   ', 'spaces': 4},
                {'text': '*   ', 'spaces': 4},
                ],
            'text': [
                {'text': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.'},
                {'text': 'Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,'},
                {'text': 'viverra nec, fringilla in, laoreet vitae, risus.'},
                {'text': 'Donec sit amet nisl. Aliquam semper ipsum sit amet velit.'},
                {'text': 'Suspendisse id sem consectetuer libero luctus adipiscing.'},
                ],
            'list_item_end': [
                {'spaces': 4},
                {'spaces': 4},
                ]
            }
        tokens = process(tokens)

        # test list 4
        expected = {
            'list_item_start': [
                {'text': '*   ', 'spaces': 4},
                {'text': '*   ', 'spaces': 4},
                ],
            'text': [
                {'text': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.'},
                {'text': 'Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,'},
                {'text': 'viverra nec, fringilla in, laoreet vitae, risus.'},
                {'text': 'Donec sit amet nisl. Aliquam semper ipsum sit amet velit.'},
                {'text': 'Suspendisse id sem consectetuer libero luctus adipiscing.'},
                ],
            'list_item_end': [
                {'spaces': 4},
                {'spaces': 4},
                ]
            }
        tokens = process(tokens)

        # test list 5
        expected = {
            'loose_item_start': [
                {'text': '*   ', 'spaces': 4},
                {'text': '*   ', 'spaces': 4},
                ],
            'text': [
                {'text': 'Codey Monkey'},
                {'text': 'Tom Cruise Crazy'},
                ],
            'list_item_end': [
                {'spaces': 4},
                {'spaces': 4},
                ]
            }
        tokens = process(token)

        # test list 5
        expected = {
            'loose_item_start': [
                {'text': '1.  ', 'spaces': 4},
                {'text': '2.  ', 'spaces': 4},
                ],
            'text': [
                {'text': 'This is a list item with two paragraphs. Lorem ipsum dolor'},
                {'text': 'sit amet, consectetuer adipiscing elit. Aliquam hendrerit'},
                {'text': 'mi posuere lectus.'},
                {'text': 'Vestibulum enim wisi, viverra nec, fringilla in, laoreet'},
                {'text': 'vitae, risus. Donec sit amet nisl. Aliquam semper ipsum'},
                {'text': 'sit amet velit.'},
                {'text': 'Suspendisse id sem consectetuer libero luctus adipiscing.'},
                ],
            'list_item_end': [
                {'spaces': 4},
                {'spaces': 4},
                ]
            }
        tokens = process(tokens)

        # test list 6
        expected = {
            'loose_item_start': [
                {'text': '*   ', 'spaces': 4},
                {'text': '*   ', 'spaces': 4},
                ],
            'text': [
                {'text': 'This is a list item with two paragraphs.'},
                {'text': 'This is the second paragraph in the list item. You\'re'},
                {'text': 'only required to indent the first line. Lorem ipsum dolor'},
                {'text': 'sit amet, consectetuer adipiscing elit.'},
                {'text': 'Another item in the same list.'},
                ],
            'list_item_end': [
                {'spaces': 4},
                {'spaces': 4},
                ]
            }
        tokens = process(tokens)

        # test list 7
        expected = {
            'loose_item_start': [
                {'text': '*   ', 'spaces': 4},
                ],
            'text': [
                {'text': 'A list item with a blockquote:'},
                ],
            'list_item_end': [
                {'spaces': 4},
                ]
            }
        tokens = process(tokens)

        # test list 7
        expected = {
            'loose_item_start': [
                {'text': '*   ', 'spaces': 4},
                ],
            'text': [
                {'text': 'A list item with a code block:'},
                ],
            'list_item_end': [
                {'spaces': 4},
                ]
            }
        tokens = process(tokens)

        # test list 7
        expected = {
            'loose_item_start': [
                {'text': '1.  ', 'spaces': 4},
                {'text': '1.  ', 'spaces': 4},
                ],
            'text': [
                {'text': 'This is a list item has a nested list.'},
                {'text': 'Lorem ipsum dolor sit amet, consectetuer adipiscing'},
                {'text': 'elit. Aliquam hendrerit mi posuere lectus.'},
                ],
            'list_item_end': [
                {'spaces': 4},
                {'spaces': 4},
                ]
            }
        tokens = process(tokens)

    def test_parse_block_quote(self):
        tokens = self._parse('blexer-blockquote.md')

        def process(tokens):
            token = tokens.pop(0)
            while token:
                type_ = token['type']

                expected_token = None
                if type_ in expected:
                    expected_token = expected[type_].pop(0)

                validate(token, expected_token)

                if type_ == 'block_quote_end':
                    break
                else:
                    token = tokens.pop(0)

            return tokens

        def validate(token, expected_token=None):
            type_ = token['type']

            if type_ == 'block_quote_start':
                assert 'text' in token
                assert 'spaces' in token
            elif type_ == 'block_quote_end':
                assert 'spaces' in token

            if not expected_token:
                return

            if 'text' in token:
                nose_tools.assert_equal(token['text'], expected_token['text'])
            if 'spaces' in token:
                nose_tools.assert_equal(token['spaces'], expected_token['spaces'])

            return

        # test blockquote 1
        expected = {
            'block_quote_start': [
                {'text': '> ', 'spaces': 2},
                ],
            'paragraph': [
                {'text': 'This is a blockquote with two paragraphs. Lorem '
                     'ipsum dolor sit amet,\nconsectetuer adipiscing '
                     'elit. Aliquam hendrerit mi posuere lectus.\nVestibulum '
                'enim wisi, viverra nec, fringilla in, laoreet vitae, risus.'},
                {'text': 'Donec sit amet nisl. Aliquam semper ipsum sit '
                     'amet velit. Suspendisse\nid sem consectetuer '
                'libero luctus adipiscing.'},
                ],
            'block_quote_end': [
                {'spaces': 2},
                ]
            }
        tokens = process(tokens)
        token = tokens.pop(0) # Remove paragraph after blockquote.

        # test blockquote 2
        expected = {
            'block_quote_start': [
                {'text': '> ', 'spaces': 2},
                ],
            'paragraph': [
                {'text': 'This is a blockquote with two paragraphs. Lorem '
                     'ipsum dolor sit amet,\nconsectetuer adipiscing '
                     'elit. Aliquam hendrerit mi posuere lectus.\nVestibulum '
                'enim wisi, viverra nec, fringilla in, laoreet vitae, risus.'},
                {'text': 'Donec sit amet nisl. Aliquam semper ipsum sit '
                     'amet velit. Suspendisse\nid sem consectetuer '
                'libero luctus adipiscing.'},
                ],
            'block_quote_end': [
                {'spaces': 2},
                ]
            }
        tokens = process(tokens)
        token = tokens.pop(0) # Remove paragraph after blockquote.

        # test blockquote 3
        expected = {
            'block_quote_start': [
                {'text': '> ', 'spaces': 2},
                {'text': '> ', 'spaces': 2},
                ],
            'paragraph': [
                {'text': 'This is the first level of quoting.'},
                {'text': 'This is nested blockquote.'},
                {'text': 'Back to the first level.'}
                ],
            'block_quote_end': [
                {'spaces': 2},
                {'spaces': 2},
                ]
            }
        tokens = process(tokens)
        tokens = process(tokens)
        token = tokens.pop(0) # Remove paragraph after blockquote.

        # test blockquote 4
        expected = {
            'block_quote_start': [
                {'text': '> ', 'spaces': 2},
                ],
            'heading': [
                {'text': '## This is a header.\n\n'}
                ],
            'list_item_start': [
                {'text': '1.   ', 'spaces': 5},
                {'text': '2.   ', 'spaces': 5}
                ],
            'text': [
                {'text': 'This is the first list item.'},
                {'text': 'This is the second list item.'}
                ],
            'list_item_end': [
                {'spaces': 5},
                {'spaces': 5}
                ],
            'paragraph': [
                {'text': 'Here\'s some example code:'}
                ],
            'code': [
                {'text': '    return shell_exec("echo $input | '
                     '$markdown_script");'}
                ],
            'block_quote_end': [
                {'spaces': 2},
                ]
            }
        tokens = process(tokens)

    def test_parse_def_links(self):
        tokens = self._parse('blexer-def-links.md')

        expected_dls = [
            '[bob]: http://bob.name/ "Bob\'s home"\n',
            '[alice]: <http://alice.name/> "Alice\'s home"\n\n',
            '[bar]: http://bar.beer/  "Foo Bar Beer"\n\n',
            '[GNU.org]: http://gnu.org\n\n',
            '  [1]: http://google.com/        "Google"\n',
            '  [2]: http://search.yahoo.com/  "Yahoo Search"\n',
            '  [3]: http://search.msn.com/    "MSN Search"\n\n',
            '  [google]: http://google.com/        "Google"\n',
            '  [yahoo]:  http://search.yahoo.com/  "Yahoo Search"\n',
            '  [msn]:    http://search.msn.com/    "MSN Search"',
            ]
        self._validate(tokens, 'def_links', expected_dls)

    def test_parse_def_footnotes(self):
        tokens = self._parse('blexer-footnotes.md')

        def process(tokens):
            token = tokens.pop(0)
            while token:
                type_ = token['type']

                expected_token = None
                if type_ in expected:
                    expected_token = expected[type_].pop(0)

                validate(token, expected_token)

                if type_ == 'footnote_end':
                    break
                else:
                    token = tokens.pop(0)

            return tokens

        def validate(token, expected_token=None):
            type_ = token['type']

            if type_ == 'footnote_start':
                assert 'multiline' in token
                assert 'spaces' in token
            elif type_ == 'footnote_end':
                assert 'spaces' in token

            if not expected_token:
                return

            if 'text' in token:
                nose_tools.assert_equal(token['text'], expected_token['text'])
            if 'spaces' in token:
                nose_tools.assert_equal(token['spaces'], expected_token['spaces'])

            return

        # test footnote 1
        expected = {
            'footnote_start': [
                {'multiline': False, 'spaces': 0},
                ],
            'paragraph': [
                {'text': 'This phrase has a single line footnote[^foot1].'},
                {'text': 'Lorem ipsum dolor sit amet, consectetuer'
                     ' adipiscing elit.'},
                ],
            'footnote_end': [
                {'spaces': 0}
                ]
            }
        tokens = process(tokens)

        # test footnote 2
        expected = {
            'footnote_start': [
                {'multiline': True, 'spaces': 4},
                ],
            'paragraph': [
                {'text': 'This other phrase has a multiline footnote[^foot2].'},
                {'text': 'Vestibulum enim wisi, viverra nec, fringilla in, '
                     'laoreet\nvitae, risus. Donec sit amet nisl. Aliquam '
                'semper ipsum sit amet\nvelit.'},
                ],
            'footnote_end': [
                {'spaces': 4}
                ]
            }
        tokens = process(tokens)

        # test footnote 3
        expected = {
            'footnote_start': [
                {'multiline': True, 'spaces': 3},
                ],
            'paragraph': [
                {'text': 'This phrase has a blockquote in its footnote[^foot3].'},
                {'text': 'A footnote with blockquotes'},
                {'text': 'Start of block quote in footnote:'},
                {'text': 'This is a blockquote with two paragraphs. Lorem'
                     ' ipsum dolor sit amet,\nconsectetuer adipiscing elit.'
                ' Aliquam hendrerit mi posuere lectus.\nVestibulum enim wisi,'
                ' viverra nec, fringilla in, laoreet vitae, risus.'},
                {'text': 'Donec sit amet nisl. Aliquam semper ipsum sit amet '
                     'velit. Suspendisse\nid sem consectetuer libero luctus '
                'adipiscing.'},
                {'text': 'End of block quote in foot note.'},
                ],
            'footnote_end': [
                {'spaces': 3}
                ]
            }
        tokens = process(tokens)

    def test_parse_block_html(self):
        tokens = self._parse('blexer-block-html.md')

        def process(tokens):
            token = tokens.pop(0)
            while token:
                type_ = token['type']

                expected_token = None
                if type_ in expected:
                    expected_token = expected[type_].pop(0)

                validate(token, expected_token)

                if type_ == 'block_html':
                    break
                else:
                    token = tokens.pop(0)

            return tokens

        def validate(token, expected_token=None):
            type_ = token['type']

            if not expected_token:
                return

            if 'text' in token:
                nose_tools.assert_equal(token['text'], expected_token['text'])
            return

        expected = {
            'block_html': [
                {
                    'text': '<table>\n    <tr>\n        <td>Monte Carlo</td>'
                    '\n    </tr>\n</table>\n\n'
                },
            ],
            }
        tokens = process(tokens)

        expected = {
            'block_html': [
                {
                    'text': '<div class="parley">\n  <article>\n    '
                    '<p>A dispute conference; human snafu.</p>\n  '
                    '</article>\n</div>\n\n'
                }
            ],
            }
        tokens = process(tokens)

        expected = {
            'block_html': [
                {'text': '<hr />\n\n'}
                ]
            }
        tokens = process(tokens)

    def test_parse_paragraph(self):
        tokens = self._parse('blexer-paragraphs.md')

        expected_ps = [
            'He used to say that there are only two sources of human '
            'vice—idleness\nand superstition, and only two '
            'virtues—activity and intelligence. He\nhimself undertook'
            ' his daughter\'s education, and to develop these '
            'two\ncardinal virtues in her gave her lessons in algebra'
            ' and geometry till\nshe was twenty, and arranged her life'
            ' so that her whole time was\noccupied. He was himself '
            'always occupied: writing his memoirs, solving\nproblems '
            'in higher mathematics, turning snuffboxes on a lathe,'
            ' working\nin the garden, or superintending the building'
            ' that was always going on\nat his estate.',

            '“Mere mobs!” repeated his new friend with a snort of'
            ' scorn. “So you\ntalk about mobs and the working classes'
            ' as if they were the\nquestion. You’ve got that eternal '
            'idiotic idea that if anarchy came it\nwould come from the'
            ' poor. Why should it? The poor have been rebels,\nbut'
            ' they have never been anarchists; they have more interest'
            ' than\nanyone else in there being some decent government.'
            ' The poor man really\nhas a stake in the country.'
            '  The rich man hasn’t; he can go away to\nNew Guinea'
            ' in a yacht. The poor have sometimes objected to '
            'being\ngoverned badly; the rich have always objected to'
            ' being governed at\nall. Aristocrats were always anarchists'
            ', as you can see from the\nbarons’ wars.”',

            'Thanking You in Advance. This sounds as if the writer'
            ' meant, "It will\nnot be worth my while to write to'
            ' you again." In making your request,\nwrite, "Will you'
            ' please," or "I shall be obliged," and if anything\nfurther'
            ' seems necessary write a letter of acknowledgment later.'
            ]

        self._validate(tokens, 'paragraph', expected_ps)

    def teardown(self):
        pass


class TestTWInlineLexer(object):

    def setup(self):
        renderer = Renderer()
        self.il = TWInlineLexer(renderer)

    def teardown(self):
        pass


class TestTWRenderer(object):

    @classmethod
    def setup_class(self):
        # temp stuff
        self.tmp_dir = tempfile.mkdtemp(suffix='md-tw-renderer-tests')
        self.del_tmp_dir = False

    def setup(self):
        self.md_wrap = TWMarkdown()

    def _write_tmp(self, file_, txt):
        with open(os.path.join(self.tmp_dir, file_), 'w') as f:
            f.write(txt)

    def _get(self, file_):
        return _get_data(file_)

    def _md(self, md_file):
        txt = self._get(md_file)
        wrapped = self.md_wrap(txt)

        self._write_tmp(md_file, wrapped)
        return wrapped

    def _validate(self, txt, expected_txt):
        txt_lines = txt.split('\n')
        txt_lines.reverse()

        for line in expected_txt.split('\n'):
            nose_tools.assert_equal(line, txt_lines.pop())

    def test_tw_obj_with_default_width(self):
        renderer = TWRenderer()

        # Check existence of textwrap.TexWrapper object.
        assert isinstance(renderer.tw, textwrap.TextWrapper)

        # Check its width
        nose_tools.assert_equal(renderer.tw.width, 72)


    def test_tw_obj_with_custom_width(self):
        renderer = TWRenderer(tw_width=80)

        # Check existence of textwrap.TexWrapper object.
        assert isinstance(renderer.tw, textwrap.TextWrapper)

        # Check its width
        nose_tools.assert_equal(renderer.tw.width, 80)


    def test_tw_set_with_valid_opts(self):
        renderer  = TWRenderer()

        # Set valid options
        renderer.tw_set(
            width=80,
            initial_indent='> ',
            subsequent_indent=' ',
            drop_whitespace=False)

        # Confirm options are set.
        nose_tools.assert_equal(renderer.tw.width, 80)
        nose_tools.assert_equal(renderer.tw.initial_indent, '> ')
        nose_tools.assert_equal(renderer.tw.subsequent_indent, ' ')
        nose_tools.assert_equal(renderer.tw.drop_whitespace, False)


    def test_tw_set_with_invalid_opts(self):
        renderer = TWRenderer()

        # Set invalid options
        renderer.tw_set(
            erase_bumps=True,
            destroy_ampersands=False,
            end_width='வருகிறேன்',
            insert_between_paragraphs='time bombs')

        # Confirm options are not set.
        nose_tools.assert_equal(getattr(renderer.tw, 'erase_bumps', None), None)
        nose_tools.assert_equal(getattr(renderer.tw, 'destroy_ampersands',
                                 None), None)
        nose_tools.assert_equal(getattr(renderer.tw, 'end_width', None), None)
        nose_tools.assert_equal(getattr(renderer.tw, 'insert_between_paragraphs',
                                 None), None)

    def test_render_paragraph(self):
        txt = self._md('renderer-paragraphs.md')
        expected_txt = self._get('renderer-paragraphs-w.md')

        self._validate(txt, expected_txt)

    def test_render_block_code(self):
        # Test block code (spaces)
        txt = self._md('renderer-block-code.md')
        expected_txt = self._get('renderer-block-code-w.md')

        self._validate(txt, expected_txt)

        # Test block code (fences)
        txt = self._md('renderer-fences.md')
        expected_txt = self._get('renderer-fences-w.md')

        self._validate(txt, expected_txt)

    def test_render_block_html(self):
        txt = self._md('renderer-block-html.md')
        expected_txt = self._get('renderer-block-html-w.md')

        self._validate(txt, expected_txt)

    def teardown(self):
        if self.del_tmp_dir:
            shutil.rmtree(self.tmp_dir)


class TestTWMarkdown(object):

    def setup(self):
        self.md = TWMarkdown()


    def test_renderer_obj(self):
        assert isinstance(self.md.renderer, TWRenderer)


    def test_inline_obj(self):
        assert isinstance(self.md.inline, TWInlineLexer)


    def test_block_obj(self):
        assert isinstance(self.md.block, TWBlockLexer)


    def teardown(self):
        pass
