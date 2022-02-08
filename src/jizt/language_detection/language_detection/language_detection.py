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

"""Language Detector.

FastText is used for langauge detection. See
`https://pypi.org/project/fasttext/`__.
"""

__version__ = '0.1.0'

import logging
import fasttext
from jizt.config import LOG_LEVEL, FASTTEXT_MODEL_PATH
from pathlib import Path
from ..models import DetectedLanguage


class LanguageDetector:
    """Language Detector.

    Args:
        _model (:obj:`fasttext.FastText._FastText`):
            The model used to detect the language.
    """

    def __init__(
        self,
        model_path: Path = FASTTEXT_MODEL_PATH,
        log_level: int = LOG_LEVEL
    ):
        self._model = fasttext.load_model(str(model_path))
        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            level=log_level,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        self.logger = logging.getLogger("LanguageDetector")

    @property
    def model(self):
        return self._model

    def detect(self, text: str) -> DetectedLanguage:
        """Predict the language of a text.

        If the text contains several languages, only the main language will be
        returned.

        Args:
            text (:obj:`str`):
                The text to detect the language of.

        Returns:
            :obj:`DetectedLanguage`: The detected language, together with the
            confidence of the prediction.
        """
        language, confidence = self._model.predict(text)
        return DetectedLanguage(
            language=language[0].split("_")[-1],
            confidence=float(confidence[0].round(2))
        )


class LanguageDetectorSingleton:
    """Singleton for :class:`LanguageDetector`.

    This singleton prevents from loading the FastText model several times.
    """

    _instance = None

    def __new__(cls) -> LanguageDetector:
        """Singleton."""
        if cls._instance is None:
            cls._instance = LanguageDetector()
        return cls._instance
