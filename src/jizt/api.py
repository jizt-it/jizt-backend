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

"""API Routes."""

__version__ = '0.1.0'

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

# v1 routes
api_router_v1 = APIRouter()

# root routes
api_router_root = APIRouter()


@api_router_root.get("/", status_code=200, response_class=HTMLResponse)
def root_view():
    return """
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Jizt API v0.0.1</h1>
            <p>Visit the docs at: <a href="https://docs.api.jizt.it">docs.api.jizt.it</a>.</p>
        </body>
    </html>
    """


@api_router_root.get("/healthz", status_code=200)
def healthcheck():
    return {"status": "alive"}
