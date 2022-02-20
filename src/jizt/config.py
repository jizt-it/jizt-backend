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

"""API Configuration."""

__version__ = '0.1.3'

import logging
from starlette.config import Config
from jizt.summaries.defaults import SummarizationDefaults
from pathlib import Path

log = logging.getLogger(__name__)
config = Config("jizt/.env")

logging.getLogger("urllib3").setLevel(logging.INFO)

LOG_LEVEL: str = config("LOG_LEVEL", default=logging.DEBUG)
ENV: str = config("ENV", default="local")

# Project's root directory
ROOT_DIR: Path = Path(__file__).parent.resolve()

# Summarization Model
SUMM_TOKENIZER_PATH: Path = config("SUMM_TOKENIZER_PATH", cast=Path, default="t5-base")
SUMM_MODEL_PATH: Path = config("SUMM_MODEL_PATH", cast=Path, default="t5-base")

# FastText Language Detection Model
FASTTEXT_MODEL_PATH: Path = config(
    "FASTTEXT_MODEL_PATH",
    cast=Path,
    default=f"{ROOT_DIR}/language_detection/language_detection/models/lid.176.ftz"
)

# Summarization defaults
SUMM_DEFAULTS: SummarizationDefaults = SummarizationDefaults()
