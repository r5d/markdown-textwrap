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

from mistune import Renderer
from nose.tools import assert_equal
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
                assert_equal(token['text'], expected.pop(0))

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
                assert_equal(token['text'], expected_token['text'])
            if 'spaces' in token:
                assert_equal(token['spaces'], expected_token['spaces'])

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

    def teardown(self):
        pass


class TestTWInlineLexer(object):

    def setup(self):
        renderer = Renderer()
        self.il = TWInlineLexer(renderer)


    def test_default_rules_contents(self):
        assert_equal(self.il.default_rules, [])


    def teardown(self):
        pass


class TestTWRenderer(object):

    def setup(self):
        pass


    def test_tw_obj_with_default_width(self):
        renderer = TWRenderer()

        # Check existence of textwrap.TexWrapper object.
        assert isinstance(renderer.tw, textwrap.TextWrapper)

        # Check its width
        assert_equal(renderer.tw.width, 72)


    def test_tw_obj_with_custom_width(self):
        renderer = TWRenderer(tw_width=80)

        # Check existence of textwrap.TexWrapper object.
        assert isinstance(renderer.tw, textwrap.TextWrapper)

        # Check its width
        assert_equal(renderer.tw.width, 80)


    def test_tw_set_options_with_valid_opts(self):
        renderer  = TWRenderer()

        # Set valid options
        renderer._tw_set_options(
            width=80,
            initial_indent='> ',
            subsequent_indent=' ',
            drop_whitespace=False)

        # Confirm options are set.
        assert_equal(renderer.tw.width, 80)
        assert_equal(renderer.tw.initial_indent, '> ')
        assert_equal(renderer.tw.subsequent_indent, ' ')
        assert_equal(renderer.tw.drop_whitespace, False)


    def test_tw_set_options_with_invalid_opts(self):
        renderer = TWRenderer()

        # Set invalid options
        renderer._tw_set_options(
            erase_bumps=True,
            destroy_ampersands=False,
            end_width='வருகிறேன்',
            insert_between_paragraphs='time bombs')

        # Confirm options are not set.
        assert_equal(getattr(renderer.tw, 'erase_bumps', None), None)
        assert_equal(getattr(renderer.tw, 'destroy_ampersands',
                                 None), None)
        assert_equal(getattr(renderer.tw, 'end_width', None), None)
        assert_equal(getattr(renderer.tw, 'insert_between_paragraphs',
                                 None), None)


    def teardown(self):
        pass


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


class TestTextWrapParagraphs(object):

    def setup(self):
        self.md = TWMarkdown()


    def test_tw_plain_paragraphs(self):
        txt = _get_data('paragraphs.md')
        expected_wrapped_txt = _get_data('paragraphs-wrapped.md')

        wrapped_txt = self.md(txt)
        assert_equal(wrapped_txt, expected_wrapped_txt)


    def test_tw_paragraphs_with_inline(self):
        txt = _get_data('paragraphs-with-inline.md')
        expected_wrapped_txt = _get_data(
            'paragraphs-with-inline-wrapped.md')

        wrapped_txt = self.md(txt)
        assert_equal(wrapped_txt, expected_wrapped_txt)


    def teardown(self):
        pass
