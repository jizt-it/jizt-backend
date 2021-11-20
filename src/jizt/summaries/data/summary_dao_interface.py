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


"""Data Access Object (DAO) interface for summaries."""

__version__ = '0.1.0'

from abc import ABC, abstractmethod
from datetime import datetime
from ..models import Summary
from typing import Tuple


class SummaryDAOInterface(ABC):
    """DAO Interface for access to :obj:`Summary` objects."""

    @abstractmethod
    def get_summary_by_summary_id(
        self,
        summary_id: str
    ) -> Summary:
        """Retrieve a summary from the database through its id.

        Args:
            summary_id (:obj:`str`):
                The summary id.

        Returns:
            :obj:tuple(:obj:`Summary`): The summary that matches the specified
            id or :obj:`None` if there is not any summary with that id.
        """

    @abstractmethod
    def get_summary_by_request_id(
        self,
        request_id: str
    ) -> Tuple[Summary, dict]:
        """Retrieve a summary from the database that matches the request id.

        Args:
            request_id (:obj:`str`):
                The request id.

        Returns:
            :obj:Tuple[:obj:`Summary`, :obj:`dict`]: A tuple with the summary
            that matches the specified request id and its associated warnings
            (if there are no warnings then they will be :obj:`None`) or a tuple
            containing two :obj:`None`s if there is not any request with the
            specified id.
        """

    @abstractmethod
    def insert_initial_request(
        self,
        request_id: str,
        summary: Summary,
        cache: bool,
        warnings: dict
    ):
        """Insert a new request to the database.

        The summary must have the same id as the request and a
        ``"preprocessing"`` status. As soon as the source text is preprocessed,
        the summary id will be updated to match this preprocessed text (hash).

        Args:
            request_id (:obj:`request_id`):
                The id of the request.
            summary (:obj:`Summary`):
                The initial (incomplete) summary.
            cache (:obj:`bool`):
                Whether the summary must be cached, i.e., permanently stored in
                the database.
            warnings (:obj:`dict`):
                The warnings derived from the user request.
        """

    @abstractmethod
    def update_summary(self,
                       request_id: str,
                       output: str,
                       output_length: int,
                       params: dict,
                       status: str,
                       started_at: datetime,
                       ended_at: datetime,
                       warnings: dict):
        """Update an existing summary.

        Args:
            request_id (:obj:`str`):
                The id of the request.
            For the rest of arguments, see :py:class:`data.models.Summary`.

        Returns:
            :obj:tuple(:obj:`Summary`, :obj:`dict`): A tuple with the updated
            summary and its associated warnings (if there are no warnings then
            they will be :obj:`None`) or a tuple containing two :obj:`None`s if
            there is not any summary with the specified id.
        """

    # @abstractmethod
    # def delete_summary(
    #     self,
    #     summary_id: str,
    #     delete_source: bool
    # ):
    #     """Delete a summary.

    #     Args:
    #         summary_id (:obj:`str`):
    #             The summary id.
    #         delete_source (:obj:`bool`):
    #             Whether to also delete the source.
    #     """

    @abstractmethod
    def update_source(
        self,
        old_source: str,
        new_source: str,
        old_summary_id: str,
        new_summary_id: str
    ):
        """Update a source text.

        Args:
            old_source (:obj:`str`):
                The previous source.
            new_source (:obj:`str`):
                The new source.
            old_summary_id (:obj:`str`):
                The old summary id.
            new_summary_id (:obj:`str`):
                The new summary id. As the source changes, so does the summary
                id. That is why this and the previous parameter must be
                provided.
        """

    @abstractmethod
    def request_exists(self, request_id: str) -> bool:
        """Determine whether a summary already exists in the database.

        Args:
            request_id (:obj:`str`):
                The request id.
        Returns:
            :obj:`bool`: Whether the summary exists or not.
        """

    @abstractmethod
    def summary_exists(self, summary_id: str):
        """Determine whether a summary already exists in the database.

        Args:
            summary_id (:obj:`str`):
                The summary id.

        Returns:
            :obj:`bool`: Whether the summary exists or not.
        """

    # @abstractmethod
    # def update_preprocessed_id(self,
    #                            raw_id: str,
    #                            new_preprocessed_id: str):
    #     """Update binding between a raw id and the preprocessed id.

    #     Aditionally to udating the binding, the summary corresponding to the old
    #     preprocessed id is deleted.

    #     Args:
    #         raw_id (:obj:`str`):
    #             The id of the summary before its source has been preprocessed.
    #         preprocessed_id (:obj:`str`):
    #             The id of the summary once its source has been preprocessed.
    #     """

    # @abstractmethod
    # def update_cache_true(self, id_: str):
    #     """Start caching a summary.

    #     If a user requests their summary not to be cached, the summary's cache
    #     value will be set to ``False``. However, if later on another user
    #     requests the same exact summary to be cached, the cache value will be
    #     set to ``True``.  The oppsite is not possible, i.e., if a user requests
    #     their summary to be cached, and then another user requests the same
    #     exact summary not to be cached, the cache value will still be ``True``,
    #     since we need to keep the summary for the user that did request the
    #     caching.

    #     Args:
    #         id_ (:obj:`str`):
    #             The raw id (not to be confused with the preprocessed id).
    #     """

    def source_exists(self, source: str):
        """Check whether a source (original text) already exists in the DB.

        Args:
            source (:obj:`str`):
                The source.

        Returns:
            :obj:`bool`: Whether the source exists or not.
        """

    def increment_summary_count(self, summary_id: str):
        """Increments the summary count.

        The summary count refers to the number of times a certain summary has
        been requested. Two summaries are considered the same if they have the
        same source text, model and parameters.

        Args:
            request_id (:obj:`str`):
                The request id.

        Returns:
            :obj:`int`: The summary count.
        """

    def delete_if_not_cache(self, id_: str):
        """Check if a summary should be cached and if not delete it.

        When requesting a summary, clients can request not to cache their
        summary.  This is useful when the user's text contains sensitive data,
        or when they simply do not want their text to be permanently stored in
        the database.

        Args:
            id_ (:obj:`str`):
                The raw id (not to be confused with the preprocessed id).
        """

    # @abstractmethod
    # def cleanup_cache(self, older_than_seconds: int):
    #     """Delete summaries with cache set to ``False`` with a certain age in seconds.

    #     Args:
    #         older_than_seconds (:obj:`int`):
    #             Maximum age in seconds of that completed summaries with cache
    #             set to ``False`` can have not to be deleted, i.e., completed
    #             summaries with cache set to ``False``and requested before
    #             ``older_than_seconds`` seconds will be deleted when calling this
    #             method.
    #     """