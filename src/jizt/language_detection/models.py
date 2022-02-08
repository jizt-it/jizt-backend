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


"""Schemas for '/language-detection' endpoint."""

__version__ = '0.1.0'

from pydantic import BaseModel


class DetectedLanguage(BaseModel):
    """Data model for the detected language.

    It also serves as schema for responses to the clients' requests.

    Attributes:
        language (:obj:`str`):
            The ISO 639-1 code of the detected language (e.g., ``"en"``).
        confidence (:obj:`float`):
            The confidence of the model when predicting the language.
    """

    language: str
    confidence: float
