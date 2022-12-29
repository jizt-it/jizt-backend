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


"""Services for '/detect-language' endpoint."""

__version__ = '0.1.0'

import logging
from jizt.config import LOG_LEVEL
from .language_detection.language_detection import LanguageDetectorSingleton
from .models import DetectedLanguage

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=LOG_LEVEL,
    datefmt='%d/%m/%Y %I:%M:%S %p'
)
logger = logging.getLogger("LanguageDetectionService")

lang_detector = LanguageDetectorSingleton()


def detect_language(text: str) -> DetectedLanguage:
    """Detect the language of a text.

    Returns:
        :obj:`models.DetectedLanguage`: the detected language (ISO-639-2), and
        the confidence of the prediction.
    """
    detected_lang = lang_detector.detect(text)
    logger.debug(
        "Language identification: [text] %s [prediction] '%s' [confidence] %s",
        text[:50], detected_lang.language, detected_lang.confidence
    )
    return detected_lang
