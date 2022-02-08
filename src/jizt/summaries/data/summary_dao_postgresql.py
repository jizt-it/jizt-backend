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


"""Summary Data Access Object (DAO) implementation for PostgreSQL."""

__version__ = '0.1.0'

import logging
import psycopg2
import hashlib
from io import StringIO
from collections import OrderedDict
from psycopg2.extras import Json
from jizt.supported_languages import SupportedLanguage
from summary_dao_interface import SummaryDAOInterface
from models import Summary
from summary_status import SummaryStatus
from supported_models import SupportedModel
from datetime import datetime


class SummaryDAOPostgresql(SummaryDAOInterface):  # TODO: manage errors in excepts
    """Summary DAO implementation for Postgresql.

    For more information, see base class.
    """

    def __init__(self, host, dbname, user, password, log_level):
        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            level=log_level,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        self.logger = logging.getLogger("SummaryDAOPostgresql")

        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
