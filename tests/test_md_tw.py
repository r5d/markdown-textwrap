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

from nose.tools import *
from pkg_resources import resource_string, resource_filename


def _get_data(f):
    rs = resource_string(__name__, '/'.join(['data', f]))
    return rs.decode()


def _get_data_path(f):
    return resource_filename(__name__, '/'.join(['data', f]))
