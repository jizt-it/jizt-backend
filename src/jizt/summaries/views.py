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


"""Views for '/summaries' endpoint."""

__version__ = '0.1.0'

from fastapi import APIRouter
from .schemas import PlainTextRequestSchema, ResponseSchema
from .service import generate_summary, get_summary

router = APIRouter()


@router.post("/plain-text", response_model=ResponseSchema)
def request_summary_view(request: PlainTextRequestSchema):
    """Request a summary of a text.

    When a client first makes a POST request, a response is given with the
    summary id. The client must then make periodic GET requests with the
    specific summary id to check the summary status. Once the summary is
    completed, the GET request will contain the output text, e.g., the summary.

    Returns:
        :obj:`schemas.ResponseSchema`: A 202 Accepted response with a JSON body
        containing the summary id, e.g.,
        ``{'summary_id': '73c3de4175449987ef6047f6e0bea91c1036a8599b'}``.

    Raises: :class:`http.client.HTTPException`:
        If the request body JSON is not valid. 
    """
    summary, warnings = generate_summary(**request.dict())
    response = summary.dict
    # Match response attribues
    if "id_" in response:
        response["summary_id"] = response.pop("id_")
    response.update(warnings)
    return response


@router.get("/plain-text/{summary_id}", response_model=ResponseSchema)
def get_summary_view(summary_id: str):
    """Get a generated summary.

    The summary status should be checked until the generation of the summary
    has been completed.

    Args:
        summary_id (:obj:`str`):
            The id of the requested summary.

    Returns:
        :obj:`schemas.ResponseSchema`: A ``200 OK`` response with a JSON body
        containing the summary. For info on the summary fields, see
        :class:`schemas.ResponseSchema`.

    Raises:
        :class:`http.client.HTTPException`: If there exists no summary with the
        specified id.
    """
    summary, warnings = get_summary(summary_id)
    response = summary.dict
    # Match response attribues
    if "id_" in response:
        response["summary_id"] = response.pop("id_")
    response.update(warnings)
    return response
