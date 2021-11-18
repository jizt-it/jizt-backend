# Copyright (C) 2020-2021 Diego Miguel Lozano <contact@jizt.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# For license information on the libraries used, see LICENSE.

"""Id generation utilities."""

__version__ = '0.1.0'

import hashlib
import random
import string


def generate_summary_id(source: str, model: str, params: dict) -> str:
    """Get a unique id for a summary.

    This method hashes the string formed by concatenating the :attr:`source`,
    :attr:`model` and :attr:`param` attributes. SHA-256 algorithm is used.

    Args:
        source (:obj:`str`):
            The ``source`` attribute in the JSON body of the request.
        model (:obj:`str`):
            The ``model`` attribute in the JSON body of the request.
        params (:obj:`dict`):
            The ``params`` attribute in the JSON body of the request.

    Returns:
        :obj:`str`: The unique, SHA-256 encrypted key.
    """

    return hashlib.sha256(
        (f"{source}{model}{str(params)}").encode()
    ).hexdigest()


def generate_request_id(source: str, model: str, params: dict) -> str:
    """Get a unique id for a summary request.

    This method hashes the string formed by concatenating the :attr:`source`,
    :attr:`model`, :attr:`param` attributes and a random value. SHA-256
    algorithm is used.

    Args:
        source (:obj:`str`):
            The ``source`` attribute in the JSON body of the request.
        model (:obj:`str`):
            The ``model`` attribute in the JSON body of the request.
        params (:obj:`dict`):
            The ``params`` attribute in the JSON body of the request.

    Returns:
        :obj:`str`: The unique, SHA-256 encrypted key.
    """
    random_string = ''.join(random.choice(string.printable) for i in range(40))
    return hashlib.sha256(
        (f"{source}{model}{str(params)}{random_string}").encode()
    ).hexdigest()


def generate_source_id(source: str) -> str:
    """Get a unique id for the source of a summary.

    This method hashes the source text. SHA-256 algorithm is used.

    Args:
        source (:obj:`str`):
            The ``source`` attribute in the JSON body of the request.

    Returns:
        :obj:`str`: The unique, SHA-256 encrypted key.
    """
    return hashlib.sha256(source.encode()).hexdigest()
