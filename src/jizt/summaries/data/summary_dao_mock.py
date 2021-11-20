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


"""Summary Data Access Object (DAO) mock implementation."""

__version__ = '0.1.0'

import logging
import hashlib
from dataclasses import dataclass
from datetime import datetime
from io import StringIO
from collections import OrderedDict
from psycopg2.extras import Json
from .summary_dao_interface import SummaryDAOInterface
from ..models import Summary
from ..utils.summary_status import SummaryStatus
from ..utils.id_generation import generate_source_id
from ..utils.supported_models import SupportedModel
from ..utils.supported_languages import SupportedLanguage
from typing import Tuple


# Table models
@dataclass
class SourceItem:
    # source_id: str (key in dict)
    content: str
    content_length: int


@dataclass
class SummaryItem:
    # summary_id: str (key in dict)
    source_id: str  # references SourceItem.source_id
    output: str
    output_length: int
    model_name: str
    params: dict
    status: str
    started_at: datetime
    ended_at: datetime
    language_tag: str
    request_count: int


@dataclass
class RequestItem:
    # request_id: str (key in dict)
    summary_id: str  # references SummaryItem.summary_id
    cache: bool
    last_accessed: datetime
    warnings: dict


class SummaryDAOMock(SummaryDAOInterface):
    """Mock Summary DAO implementation for Postgresql.

    For more information, see base class.
    """

    def __init__(self, log_level):
        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            level=log_level,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        self.logger = logging.getLogger("SummaryDAOPostgresql")
        # Mock tables (dicts with keys as ids)
        self.SOURCE_TABLE = {}
        self.SUMMARY_TABLE = {}
        self.REQUEST_TABLE = {}

    def request_exists(self, request_id: str) -> bool:
        """See base class."""
        return request_id in self.REQUEST_TABLE

    def summary_exists(self, summary_id: str) -> bool:
        """See base class."""
        return summary_id in self.SUMMARY_TABLE

    def get_summary_by_summary_id(  # TODO: use get_summary_by_request_id instead
        self,
        summary_id: str
    ) -> Tuple[Summary, dict]:
        """See base class."""
        if not self.summary_exists(summary_id):
            return None, None
        summary = self.SUMMARY_TABLE[summary_id]
        summary = Summary(summary_id, self.SOURCE_TABLE[summary.source_id],
                          summary.output, SupportedModel(summary.model_name),
                          summary.params, SummaryStatus(summary.status),
                          summary.started_at, summary.ended_at,
                          SupportedLanguage(summary.language_tag))
        return summary, None

    def get_summary_by_request_id(
        self,
        request_id: str
    ) -> Tuple[Summary, dict]:
        """See base class."""
        if not self.request_exists(request_id):
            return None, None
        request = self.REQUEST_TABLE[request_id]
        # The summary id should always exist. Otherwise, there's been a
        # programming error. If it happened, we could delete the request and
        # return an error.
        summary_id = request.summary_id
        if not self.summary_exists(summary_id):
            return None, None
        summary = self.SUMMARY_TABLE[summary_id]
        summary = Summary(summary_id, self.SOURCE_TABLE[summary.source_id],
                          summary.output, SupportedModel(summary.model_name),
                          summary.params, SummaryStatus(summary.status),
                          summary.started_at, summary.ended_at,
                          SupportedLanguage(summary.language_tag))
        return summary, request.warnings

    def increment_summary_count(self, summary_id: str):
        """See base class."""
        if not self.summary_exists(summary_id):
            return
        self.SUMMARY_TABLE[summary_id].request_count += 1

    def insert_initial_request(
        self,
        request_id: str,
        summary: Summary,
        cache: bool,
        warnings: dict
    ):
        """See base class."""
        self.REQUEST_TABLE[request_id] = RequestItem(summary.id_,
                                                     cache,
                                                     datetime.now(),
                                                     warnings)
        source_id = generate_source_id(summary.source)
        self.SUMMARY_TABLE[summary.id_] = SummaryItem(
            source_id,
            summary.output,
            None if not summary.output else len(summary.output),
            summary.model,
            summary.params,
            summary.status,
            summary.started_at,
            summary.ended_at,
            summary.language,
            1
        )
        self.SOURCE_TABLE[source_id] = SourceItem(summary.source,
                                                  len(summary.source))

    def update_summary(
        self,
        request_id: str,
        output: str = None,
        output_length = None,
        params: dict = None,
        status: str = None,
        started_at: datetime = None,
        ended_at: datetime = None,
        warnings: dict = None
    ):
        """See base class."""
        if request_id in self.REQUEST_TABLE:
            args = OrderedDict({key: value for key, value in locals().items()
                                if value is not None
                                   and key not in ('self', 'request_id')})
            if "warnings" in args:
                self.REQUEST_TABLE[request_id].warnings = args.pop("warnings")
            summary_id = self.REQUEST_TABLE[request_id].summary_id
            summary = self.SUMMARY_TABLE[summary_id]
            _ = [setattr(summary, arg, args[arg]) for arg in args]
            self.SUMMARY_TABLE[summary_id] = summary

    def update_source(
        self,
        old_source: str,
        new_source: str,
        old_summary_id: str,
        new_summary_id: str
    ):
        """See base class."""
        # Update summary_ids in requests table
        update_request = {
            request_id: RequestItem(new_summary_id, request.cache,
                                    datetime.now(), request.warnings)
            for request_id, request in self.REQUEST_TABLE.items()
            if request.summary_id == old_summary_id
        }
        self.REQUEST_TABLE.update(update_request)
        # Update summary_ids in summaries table
        self.SUMMARY_TABLE[new_summary_id] = self.SUMMARY_TABLE.pop(old_summary_id)
        # Update source_id in source table
        old_source_id = self._get_unique_key(old_source)
        new_source_id = self._get_unique_key(new_source)
        self.SOURCE_TABLE[new_source_id] = self.SOURCE_TABLE.pop(old_source_id)

    @classmethod
    def _get_unique_key(cls, text: str) -> str:
        """Get a unique key for a text. SHA-256 algorithm is used.

        Args:
            text (:obj:`str`):
                The text to get the unique id from.

        Returns:
            :obj:`str`: The unique, SHA-256 ecrypted key.
        """
        return hashlib.sha256(text.encode()).hexdigest()
