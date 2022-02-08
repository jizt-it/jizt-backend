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


"""Schemas for '/summaries' endpoint."""

__version__ = '0.1.0'

from datetime import datetime
from pydantic import BaseModel
from .utils.supported_models import SupportedModel
from .utils.supported_languages import SupportedLanguage
from .utils.summary_status import SummaryStatus
from typing import Any, Dict, List, Optional, Union


class Summary():
    """Summary class.

    Attributes:
        id_ (:obj:`str`):
            The id of the summary.
        source (:obj:`str`):
            The source to process, e.g., a plain text to be summarized.
        output (:obj:`str`):
            The output once the source has been processed, e.g., a summary.
        model (:obj:`utils.supported_models.SupportedModel`):
            The model with which the summary was generated.
        params (:obj:`dict`):
            The parameters with which the summary was generated.
        status (:obj:`utils.summary_status.SummaryStatus`):
            The current status of the summary.
        started_at (:obj:`datetime.datetime`):
            The time when the summary was first requested.
        ended_at (:obj:`datetime.datetime`):
            The time when the summary first finished.
        language (:obj:utils.supported_languages.SupportedLanguage):
            The language of the summary.
    """

    def __init__(
        self,
        id_: str,
        source: str,
        output: str,
        model: SupportedModel,
        params: Dict[str, Union[bool, int, float]],
        status: SummaryStatus,
        started_at: datetime,
        ended_at: datetime,
        language: SupportedLanguage
    ):  # 2020 be like
        self.id_ = id_
        self.source = source
        self.output = output
        self.model = model.value
        self.params = params
        self.status = status.value
        self.started_at = started_at
        self.ended_at = ended_at
        self.language = language.value

    def dict(self):
        """Return summary object as :obj:`dict`."""
        return self.__dict__

    def __str__(self):
        return (f'SUMMARY [id]: {self.id_}, [source]: "{self.source}", '
                f'[output]: "{self.output}", [model]: {self.model}, '
                f'[params]: {self.params}, [status]: {self.status}, '
                f'[started_at]: {self.started_at}, [ended_at]: {self.ended_at}, '
                f'[language]: {self.language}')

    def __repr__(self):
        return (f'Summary({self.id_}, {self.source}, {self.output}, '
                f'{self.model}, {self.params}, {self.status}, {self.started_at}, '
                f'{self.ended_at}, {self.language}')


class PlainTextRequestSchema(BaseModel):
    """Schema for the clients' plain-text REST requests.

    :code:`/v1/summaries/plain_text - POST`

    Attributes:
        source (:obj:`str`):
            The text in plain format to be summarized.
        model (:obj:`utils.supported_models.SupportedModel`, `optional`,
               defaults to :obj:`utils.supported_models.SupportedModel.T5`):
            The model used to generate the summary.
        params (:obj:`dict`, `optional`, defaults to :obj:`{}`):
            The params used in the summary generation.
        language (:obj:utils.supported_languages.SupportedLanguage, `optional`,
                  defaults to :obj:utils.supported_languages.SupportedLanguag.ENGLISH):
            The language of the text.
        cache (:obj:`bool`), `optional`, defaults to :obj:`True`):
            Whether the summary must be cached or not. A cached summary implies
            that it will be permanently stored in the database.
    """

    source: str
    model: Optional[SupportedModel] = SupportedModel.T5
    params: Optional[Dict[str, Any]] = {}
    language: Optional[SupportedLanguage] = SupportedLanguage.ENGLISH
    cache: Optional[bool]


class ResponseSchema(BaseModel):
    """Schema for the response to the clients' requests.

    Some of the fields might not be available during the generation of the
    summary, e.g. ``output`` or ``ended_at``. Once the summary is ready, the
    ``status`` will change to ``completed`` and the missing fields will be
    available then.

    Attributes:
        summary_id (:obj:`str`):
            The id of the summary.
        started_at (:obj:`datetime.datetime`):
            The time when the summary was first created.
        ended_at (:obj:`datetime.datetime`):
            The time when the summary first finished.
        status (:obj:`utils.summary_status.SummaryStatus`):
            The current status of the summary.
        output (:obj:`str`):
            The processed text, e.g., the summary.
        model (:obj:`utils.supported_models.SupportedModel`):
            The model with wich the summary was generated.
        params (:obj:`dict`):
            The parameters with which the summary was generated.
        language (:obj:utils.supported_languages.SupportedLanguage):
            The language of the summary.
        warnings (:obj:`dict`):
            The warnings derived from the client's request (if any).
    """

    summary_id: str
    started_at: datetime
    ended_at: Optional[datetime]
    status: SummaryStatus
    output: Optional[str]
    model: SupportedModel
    params: Dict[str, Any] = {}
    language: SupportedLanguage
    warnings: Dict[str, List[str]]
