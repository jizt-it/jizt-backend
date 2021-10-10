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

"""Jizt REST API.

Find the documentation at `https://docs.api.jizt.it`__.
"""

__version__ = '0.1.2'

import logging
from starlette.applications import Starlette
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jizt.api import api_router_root, api_router_v1
from jizt.logging import configure_logging

log = logging.getLogger(__name__)
configure_logging()

app = Starlette()
api_root = FastAPI(title="Jizt REST API")
api_v1 = FastAPI(
    title="Jizt REST API",
    version="0.0.2",
    # Disable docs
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    # Origins examples: http://jizt.it, https://app.jizt.it, http://jizt.it/hi
    allow_origins=r"https?://\w*\.?jizt\.it/?.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['Content-Type'],
)

# Include routes
api_root.include_router(api_router_root)
api_v1.include_router(api_router_v1)

# Mount API routes
# Order matters! More specific routes must come first.
app.mount("/api/v1", app=api_v1)
app.mount("/", app=api_root)
