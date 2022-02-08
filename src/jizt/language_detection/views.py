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


"""Views for '/language-detection' endpoint."""

__version__ = '0.1.0'

import logging
from fastapi import APIRouter, Response, status
from jizt.config import LOG_LEVEL
from .models import DetectedLanguage
from .service import detect_language

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=LOG_LEVEL,
    datefmt='%d/%m/%Y %I:%M:%S %p'
)
logger = logging.getLogger("LanguageDetectionViews")
router = APIRouter()


@router.post("", response_model=DetectedLanguage)
async def detect_language_view(
    response: Response,
    text: str = ""
) -> DetectedLanguage:
    """Detect the language of a text.

    Args:
        text (:obj:`str`):
            The text to detect the language of.

    Returns:
        :obj:`models.DetectedLanguage`: A 200 OK response with a JSON body
        containing the detected language (ISO-639-2), as well as the confidence
        score::

           ``{"language": "en", "confidence": 0.98}``

        If the text is empty, a 204 No Content (without body) is returned.
    """
    if text:
        return detect_language(text)
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
