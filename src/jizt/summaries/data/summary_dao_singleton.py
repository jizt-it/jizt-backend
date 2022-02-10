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


"""Singleton providing a Data Access Object (DAO) for summaries."""

__version__ = '0.1.0'

import logging
# from .summary_dao_postgresql import SummaryDAOPostgresql
from .summary_dao_mock import SummaryDAOMock


class SummaryDAOSingleton:
    """Summary DAO Singleton."""

    _instance = None

    def __new__(cls, log_level: int = logging.ERROR) -> SummaryDAOMock:
        """Singleton.

        Args:
            log_level (:obj:`int`, `optional`, defaults to `logging.ERROR`):
                The log level.

        Returns:
            :obj:`SummaryDAOPostgresql`: The single instance of the DAO.
        """

        if cls._instance is None:
            cls._instance = SummaryDAOMock(log_level)
        return cls._instance
