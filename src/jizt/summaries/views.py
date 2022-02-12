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

__version__ = '0.1.1'

import logging
from fastapi import (APIRouter, HTTPException, BackgroundTasks, Depends,
                     Response, status)
from jizt.config import LOG_LEVEL
from jizt.supported_languages import SupportedLanguage
from jizt.language_detection.language_detection.language_detection import \
    LanguageDetectorSingleton
from .models import PlainTextRequestSchema, ResponseSchema, Summary
from .service import generate_summary, get_summary

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=LOG_LEVEL,
    datefmt='%d/%m/%Y %I:%M:%S %p'
)
logger = logging.getLogger("SummaryViews")
router = APIRouter()

lang_detector = LanguageDetectorSingleton()


@router.post("/plain-text", response_model=ResponseSchema,
             status_code=status.HTTP_202_ACCEPTED)
async def request_summary_view(
    request: PlainTextRequestSchema,
    response: Response,
    background_tasks: BackgroundTasks,
    result: tuple[Summary, dict] = Depends(generate_summary)  # TODO: model for warnings
) -> ResponseSchema:
    """Request a summary of a text.

    When a client first makes a POST request, a response is given with the
    summary id. The client must then make periodic GET requests with the
    specific summary id to check the summary status. Once the summary is
    completed, the GET request will contain the output text, e.g., the summary.

    Returns:
        :obj:`models.ResponseSchema`: A 202 Accepted response with a JSON body
        containing the summary id, e.g.,
        ``{'summary_id': '73c3de4175449987ef6047f6e0bea91c1036a8599b'}``.

    Raises: :class:`http.client.HTTPException`:
        If the request is not valid.
    """
    if not request.source:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    language = lang_detector.detect(request.source).language
    if not SupportedLanguage.is_supported(language):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"detected language '{language}' not supported"
        )

    summary, warnings = result
    response = summary.dict().copy()
    # Match response attributes
    response["summary_id"] = response.pop("id_")
    # response.update(warnings)  # TODO
    response["warnings"] = {}  # TODO: delete
    return response


@router.get("/plain-text/{summary_id}", response_model=ResponseSchema)
async def get_summary_view(summary_id: str):
    """Get a generated summary.

    The summary status should be checked until the generation of the summary
    has been completed.

    Args:
        summary_id (:obj:`str`):
            The id of the requested summary.

    Returns:
        :obj:`models.ResponseSchema`: A ``200 OK`` response with a JSON body
        containing the summary. For info on the summary fields, see
        :class:`models.ResponseSchema`.

    Raises:
        :class:`http.client.HTTPException`: If there exists no summary with the
        specified id.
    """
    summary, warnings = get_summary(summary_id)
    if summary is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Summary '{summary_id}' not found.")
    response = summary.dict().copy()
    # Match response attributes
    response.pop("id_")
    response["summary_id"] = summary_id  # match the request id
    # response.update(warnings)  # TODO
    response["warnings"] = {}  # TODO: delete
    return response
